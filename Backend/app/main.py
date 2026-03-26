"""
Finance & AI Calculator Platform Backend
FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

load_dotenv()

# ── Firebase Admin init ───────────────────────────────────────────────────────
import json

try:
    firebase_admin.get_app()
except ValueError:
    firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
    if firebase_creds:
        cred_dict = json.loads(firebase_creds)
        _cred = credentials.Certificate(cred_dict)
    else:
        _cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(_cred)

# ── App imports ───────────────────────────────────────────────────────────────
from app.services.calculator_router import CalculatorRegistry
from app.routers import loan, investment, tax, other, assistant
from app.db.database import engine, get_db
from app.db.models import Base, CalculationHistory

from app.calculators.emi import calculate_emi, calculate_emi_for_payment
from app.calculators.sip import calculate_sip, calculate_lumpsum
from app.calculators.cagr import calculate_cagr, calculate_required_return
from app.calculators.fd import calculate_fd
from app.calculators.rd import calculate_rd, calculate_rd_simple
from app.calculators.tax import (
    calculate_tax_old_regime,
    calculate_tax_new_regime,
    compare_tax_regimes,
)
from app.calculators.other import (
    calculate_inflation_adjusted_value,
    calculate_future_value_with_inflation,
    calculate_retirement_corpus,
    calculate_retirement_corpus_with_existing_savings,
)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Finance & AI Calculator Platform",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

Base.metadata.create_all(bind=engine)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loan.router,       prefix="")
app.include_router(investment.router, prefix="")
app.include_router(tax.router,        prefix="")
app.include_router(other.router,      prefix="")
app.include_router(assistant.router)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_firebase_uid(request: Request) -> str | None:
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        print(f"AUTH HEADER: '{token[:30] if token else 'EMPTY'}'")  # ADD THIS
        if not token:
            return None
        decoded = firebase_auth.verify_id_token(token)
        return decoded.get("uid")
    except Exception as e:
        print(f"AUTH ERROR: {e}")  # ADD THIS
        return None


def save_history(db: Session, request: Request, calc_type: str, calc_name: str,
                 inputs: dict, result: dict):
    try:
        uid = get_firebase_uid(request)
        print(f"SAVE_HISTORY: uid={uid}, type={calc_type}")  # ADD THIS
        if not uid:
            print("SAVE_HISTORY: No uid, skipping")  # ADD THIS
            return
        record = CalculationHistory(
            user_id=uid,
            calculator_type=calc_type,
            calculator_name=calc_name,
            inputs=inputs,
            result=result,
        )
        db.add(record)
        db.commit()
        print(f"SAVE_HISTORY: Saved successfully")  # ADD THIS
    except Exception as e:
        print(f"History save skipped: {e}")

# ── Basic routes ──────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/calculators")
async def list_calculators():
    calculators = CalculatorRegistry.list_calculators()
    return {"total": len(calculators), "calculators": calculators}


@app.get("/api/calculators/{calculator_type}")
async def get_calculator(calculator_type: str):
    try:
        info = CalculatorRegistry.get_calculator_info(calculator_type)
        return {
            "type": calculator_type,
            "name": info["description"],
            "description": info["description"],
            "inputs": []
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── History routes ────────────────────────────────────────────────────────────
@app.get("/api/history")
async def get_history(
    request: Request,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    uid = get_firebase_uid(request)
    if not uid:
        raise HTTPException(status_code=401, detail="Authentication required")

    records = (
        db.query(CalculationHistory)
        .filter(CalculationHistory.user_id == uid)
        .order_by(CalculationHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "total": len(records),
        "history": [
            {
                "id":              str(r.id),
                "calculator_type": r.calculator_type,
                "calculator_name": r.calculator_name,
                "inputs":          r.inputs,
                "result":          r.result,
                "created_at":      r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ]
    }


@app.delete("/api/history/{record_id}")
async def delete_history_record(
    record_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    uid = get_firebase_uid(request)
    if not uid:
        raise HTTPException(status_code=401, detail="Authentication required")

    record = db.query(CalculationHistory).filter(
        CalculationHistory.id == record_id,
        CalculationHistory.user_id == uid
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
    return {"deleted": True}


# ── Unified calculator route ───────────────────────────────────────────────────
TYPE_ALIASES = {
    "reverse_emi":                    "reverse-emi",
    "required_return":                "required-return",
    "rd_simple":                      "rd-simple",
    "tax_old":                        "tax-old",
    "tax_old_regime":                 "tax-old",
    "income_tax_old_regime":          "tax-old",
    "tax_new":                        "tax-new",
    "tax_new_regime":                 "tax-new",
    "income_tax_new_regime":          "tax-new",
    "tax_compare":                    "tax-compare",
    "tax_comparison":                 "tax-compare",
    "compare_tax_regimes":            "tax-compare",
    "future_value_inflation":         "future-value-inflation",
    "future_value_with_inflation":    "future-value-inflation",
    "retirement_corpus":              "retirement-corpus",
    "retirement_with_savings":        "retirement-with-savings",
    "retirement_corpus_with_savings": "retirement-with-savings",
    "inflation_adjusted":             "inflation",
    "inflation_adjusted_value":       "inflation",
    "lumpsum_investment":             "lumpsum",
    "cagr_calculator":                "cagr",
    "emi_calculator":                 "emi",
    "sip_calculator":                 "sip",
    "fd_calculator":                  "fd",
    "rd_calculator":                  "rd",
}

CALC_NAMES = {
    "emi":                    "EMI Calculator",
    "reverse-emi":            "Reverse EMI Calculator",
    "sip":                    "SIP Calculator",
    "lumpsum":                "Lumpsum Investment Calculator",
    "cagr":                   "CAGR Calculator",
    "required-return":        "Required Return Calculator",
    "fd":                     "Fixed Deposit Calculator",
    "rd":                     "Recurring Deposit Calculator",
    "rd-simple":              "RD Calculator (Simplified)",
    "tax-old":                "Income Tax (Old Regime)",
    "tax-new":                "Income Tax (New Regime)",
    "tax-compare":            "Tax Regime Comparison",
    "roi":                    "ROI Calculator",
    "inflation":              "Inflation Adjusted Value",
    "future-value-inflation": "Future Value with Inflation",
    "retirement-corpus":      "Retirement Corpus Calculator",
    "retirement-with-savings":"Retirement with Savings",
}


@app.post("/api/calculators/{calculator_type}")
async def calculate_unified(
    calculator_type: str,
    request: Request,
    db: Session = Depends(get_db)
):
    body: dict = await request.json()
    raw_t = calculator_type.lower().strip()
    t = TYPE_ALIASES.get(raw_t, raw_t.replace("_", "-"))

    def get(key: str, required: bool = True) -> float:
        val = body.get(key)
        if val is None:
            if required:
                raise HTTPException(
                    status_code=422,
                    detail=f"Missing required field '{key}' for '{t}'"
                )
            return 0.0
        try:
            return float(val)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=422,
                detail=f"Field '{key}' must be a number, got: {val!r}"
            )

    def flatten(raw: dict) -> dict:
        if isinstance(raw.get("result"), dict):
            return dict(raw["result"])
        return raw

    def done(result: dict) -> dict:
        save_history(db, request, t, CALC_NAMES.get(t, t), body, result)
        return result

    try:

        # ── EMI ───────────────────────────────────────────────────────────────
        if t == "emi":
            raw = calculate_emi(
                principal=get("principal"),
                annual_interest_rate=get("rate"),
                tenure_months=int(get("tenure"))
            )
            r = flatten(raw)
            return done({
                "Monthly EMI":      r.get("emi") or r.get("monthly_emi"),
                "Total Payment":    r.get("total_payment") or r.get("total_amount"),
                "Total Interest":   r.get("total_interest"),
                "Principal Amount": get("principal"),
            })

        # ── REVERSE EMI ───────────────────────────────────────────────────────
        elif t == "reverse-emi":
            raw = calculate_emi_for_payment(
                principal=get("principal"),
                annual_interest_rate=get("rate"),
                monthly_emi=get("monthly_emi")
            )
            r = flatten(raw)
            return done({
                "Required Tenure (months)": r.get("tenure_months") or r.get("required_tenure"),
                "EMI Amount":               r.get("emi") or get("monthly_emi"),
                "Total Payment":            r.get("total_payment") or r.get("total_amount"),
                "Total Interest":           r.get("total_interest"),
            })

        # ── SIP ───────────────────────────────────────────────────────────────
        elif t == "sip":
            monthly      = get("monthly_investment")
            tenure_years = get("tenure")
            raw = calculate_sip(
                monthly_investment=monthly,
                annual_return_rate=get("rate"),
                tenure_months=int(tenure_years * 12)
            )
            r = flatten(raw)
            return done({
                "Maturity Value":     r.get("maturity_value"),
                "Total Invested":     r.get("invested_amount"),
                "Wealth Gained":      r.get("earnings"),
                "Monthly Investment": monthly,
            })

        # ── LUMPSUM ───────────────────────────────────────────────────────────
        elif t == "lumpsum":
            principal    = get("principal")
            tenure_years = get("tenure")
            raw = calculate_lumpsum(
                principal=principal,
                annual_return_rate=get("rate"),
                tenure_months=int(tenure_years * 12)
            )
            r = flatten(raw)
            return done({
                "Maturity Value":    r.get("maturity_value"),
                "Principal":         r.get("principal") or principal,
                "Earnings":          r.get("earnings"),
                "Absolute Return %": r.get("absolute_return_percentage"),
            })

        # ── CAGR ──────────────────────────────────────────────────────────────
        elif t == "cagr":
            raw = calculate_cagr(
                beginning_value=get("beginning_value"),
                ending_value=get("ending_value"),
                tenure_years=get("tenure")
            )
            r = flatten(raw)
            return done({
                "CAGR %":          r.get("cagr") or r.get("cagr_percentage"),
                "Beginning Value": get("beginning_value"),
                "Ending Value":    get("ending_value"),
                "Absolute Return": round(get("ending_value") - get("beginning_value"), 2),
            })

        # ── REQUIRED RETURN ───────────────────────────────────────────────────
        elif t == "required-return":
            raw = calculate_required_return(
                beginning_value=get("beginning_value"),
                target_ending_value=get("target_ending_value"),
                tenure_years=get("tenure")
            )
            r = flatten(raw)
            return done({
                "Required Annual Return %": r.get("required_return") or r.get("required_annual_return"),
                "Beginning Value":          get("beginning_value"),
                "Target Value":             get("target_ending_value"),
                "Period (years)":           get("tenure"),
            })

        # ── FIXED DEPOSIT ─────────────────────────────────────────────────────
        elif t == "fd":
            tenure_years = get("tenure")
            raw = calculate_fd(
                principal=get("principal"),
                annual_interest_rate=get("rate"),
                tenure_months=int(tenure_years * 12),
                compounding_frequency="quarterly"
            )
            r = flatten(raw)
            return done({
                "Maturity Value":   r.get("maturity_value"),
                "Interest Earned":  r.get("interest_earned"),
                "Principal":        r.get("principal") or get("principal"),
                "Effective Rate %": r.get("effective_annual_rate"),
            })

        # ── RECURRING DEPOSIT ─────────────────────────────────────────────────
        elif t == "rd":
            monthly       = get("monthly_amount")
            tenure_months = int(get("tenure"))
            raw = calculate_rd(
                monthly_deposit=monthly,
                annual_interest_rate=get("rate"),
                tenure_months=tenure_months,
                compounding_frequency="quarterly"
            )
            r = flatten(raw)
            return done({
                "Maturity Value":  r.get("maturity_value"),
                "Total Invested":  r.get("total_deposited") or r.get("invested_amount") or round(monthly * tenure_months, 2),
                "Interest Earned": r.get("interest_earned") or r.get("total_interest"),
                "Monthly Deposit": monthly,
            })

        # ── RD SIMPLIFIED ─────────────────────────────────────────────────────
        elif t == "rd-simple":
            monthly       = get("monthly_amount")
            tenure_months = int(get("tenure"))
            raw = calculate_rd_simple(
                monthly_deposit=monthly,
                annual_interest_rate=get("rate"),
                tenure_months=tenure_months
            )
            r = flatten(raw)
            return done({
                "Maturity Value":  r.get("maturity_value"),
                "Total Invested":  r.get("total_deposited") or r.get("invested_amount") or round(monthly * tenure_months, 2),
                "Interest Earned": r.get("interest_earned") or r.get("total_interest"),
                "Monthly Deposit": monthly,
            })

        # ── TAX OLD REGIME ────────────────────────────────────────────────────
        elif t == "tax-old":
            raw = calculate_tax_old_regime(
                gross_income=get("income"),
                age=int(get("age"))
            )
            r = flatten(raw)
            total_tax = r.get("total_tax_liability") or r.get("total_tax") or r.get("tax_payable") or 0
            return done({
                "Gross Income":     get("income"),
                "Taxable Income":   r.get("taxable_income") or get("income"),
                "Income Tax":       r.get("income_tax") or r.get("base_tax") or 0,
                "Cess (4%)":        r.get("cess") or r.get("education_cess") or 0,
                "Total Tax":        total_tax,
                "Effective Rate %": r.get("effective_tax_rate") or r.get("effective_rate") or 0,
                "Monthly Tax":      round(total_tax / 12, 2),
            })

        # ── TAX NEW REGIME ────────────────────────────────────────────────────
        elif t == "tax-new":
            raw = calculate_tax_new_regime(
                gross_income=get("income"),
                age=int(get("age"))
            )
            r = flatten(raw)
            total_tax = r.get("total_tax_liability") or r.get("total_tax") or r.get("tax_payable") or 0
            return done({
                "Gross Income":     get("income"),
                "Taxable Income":   r.get("taxable_income") or get("income"),
                "Income Tax":       r.get("income_tax") or r.get("base_tax") or 0,
                "Cess (4%)":        r.get("cess") or r.get("education_cess") or 0,
                "Total Tax":        total_tax,
                "Effective Rate %": r.get("effective_tax_rate") or r.get("effective_rate") or 0,
                "Monthly Tax":      round(total_tax / 12, 2),
            })

        # ── TAX COMPARISON ────────────────────────────────────────────────────
        elif t == "tax-compare":
            raw = compare_tax_regimes(
                gross_income=get("income"),
                age=int(get("age"))
            )
            r = flatten(raw)
            return done({
                "Old Regime Tax": r.get("old_regime_tax") or r.get("old_tax") or 0,
                "New Regime Tax": r.get("new_regime_tax") or r.get("new_tax") or 0,
                "Better Regime":  r.get("better_regime") or r.get("recommended_regime") or "Check results",
                "Tax Savings":    r.get("tax_savings") or r.get("savings") or 0,
                "Gross Income":   get("income"),
            })

        # ── ROI ───────────────────────────────────────────────────────────────
        elif t == "roi":
            initial  = get("initial_investment")
            final    = get("final_value")
            tenure   = get("tenure")
            if initial <= 0:
                raise HTTPException(status_code=422, detail="initial_investment must be greater than 0")
            profit   = final - initial
            roi_pct  = (profit / initial) * 100
            cagr_val = ((final / initial) ** (1 / tenure) - 1) * 100 if tenure > 0 else 0.0
            return done({
                "ROI %":              round(roi_pct, 2),
                "CAGR %":             round(cagr_val, 2),
                "Profit / Loss":      round(profit, 2),
                "Initial Investment": round(initial, 2),
                "Final Value":        round(final, 2),
            })

        # ── INFLATION ADJUSTED ────────────────────────────────────────────────
        elif t == "inflation":
            raw = calculate_inflation_adjusted_value(
                current_value=get("current_value"),
                annual_inflation_rate=get("annual_inflation_rate"),
                tenure_years=get("tenure")
            )
            r = flatten(raw)
            return done({
                "Current Value":            get("current_value"),
                "Inflation-Adjusted Value": r.get("inflation_adjusted_value") or r.get("adjusted_value"),
                "Purchasing Power Loss":    r.get("purchasing_power_loss") or r.get("value_lost"),
                "Loss %":                   r.get("loss_percentage") or r.get("purchasing_power_loss_percentage"),
            })

        # ── FUTURE VALUE WITH INFLATION ───────────────────────────────────────
        elif t == "future-value-inflation":
            raw = calculate_future_value_with_inflation(
                current_value=get("current_value"),
                annual_return_rate=get("annual_return_rate"),
                annual_inflation_rate=get("annual_inflation_rate"),
                tenure_years=get("tenure")
            )
            r = flatten(raw)
            return done({
                "Nominal Future Value": r.get("nominal_future_value") or r.get("future_value"),
                "Real Future Value":    r.get("real_future_value") or r.get("inflation_adjusted_value"),
                "Current Value":        get("current_value"),
                "Inflation Impact":     r.get("inflation_impact") or r.get("value_eroded_by_inflation"),
            })

        # ── RETIREMENT CORPUS ─────────────────────────────────────────────────
        elif t == "retirement-corpus":
            raw = calculate_retirement_corpus(
                monthly_expense=get("monthly_expense"),
                annual_inflation_rate=get("annual_inflation_rate"),
                years_in_retirement=get("years_in_retirement"),
                annual_return_rate=get("annual_return_rate")
            )
            r = flatten(raw)
            return done({
                "Required Corpus":       r.get("required_corpus") or r.get("corpus_required"),
                "Monthly Expense Today": get("monthly_expense"),
                "Years in Retirement":   get("years_in_retirement"),
                "Monthly Withdrawal":    r.get("monthly_withdrawal") or r.get("first_year_monthly_withdrawal"),
            })

        # ── RETIREMENT WITH SAVINGS ───────────────────────────────────────────
        elif t == "retirement-with-savings":
            raw = calculate_retirement_corpus_with_existing_savings(
                monthly_expense=get("monthly_expense"),
                annual_inflation_rate=get("annual_inflation_rate"),
                years_to_retirement=get("years_to_retirement"),
                years_in_retirement=get("years_in_retirement"),
                existing_savings=get("existing_savings"),
                annual_return_before_retirement=get("annual_return_before_retirement"),
                annual_return_in_retirement=get("annual_return_in_retirement")
            )
            r = flatten(raw)
            shortfall = r.get("shortfall_or_surplus") or r.get("corpus_gap") or 0
            return done({
                "Required Corpus":         r.get("required_corpus") or r.get("corpus_required"),
                "Future Value of Savings": r.get("future_value_of_savings") or r.get("savings_future_value"),
                "Shortfall / Surplus":     shortfall,
                "Status":                  r.get("status") or ("Surplus" if shortfall >= 0 else "Shortfall"),
            })

        else:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown calculator type: '{t}'"
            )

    except HTTPException:
        raise
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {e}")


# ── Error handler ─────────────────────────────────────────────────────────────
@app.exception_handler(HTTPException)
async def http_error(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
