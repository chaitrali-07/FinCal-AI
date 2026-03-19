"""
FastAPI routes for investment calculators.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.schemas.investment_schema import (
    SIPRequest, LumpsumRequest, CAGRRequest, RequiredReturnRequest,
    TenureForCAGRRequest, FDRequest, FDWithPayoutRequest, RDRequest,
    RDSimpleRequest, RequiredMonthlyDepositRequest, InvestmentResponse
)
from app.calculators import sip, cagr, fd, rd
from app.db.database import get_db
from app.db.models import CalculationHistory
from app.services.auth import AuthService

router = APIRouter(prefix="/api/calculate/investment", tags=["Investment Calculators"])


def save_calculation_to_history(
    db: Session,
    token: Optional[str],
    calculator_type: str,
    calculator_name: str,
    inputs: Dict[str, Any],
    result: Dict[str, Any]
):
    """Helper function to save calculation to history"""
    if token:
        try:
            decoded_token = AuthService.verify_token(token)
            user_id = decoded_token.get("uid")
            
            history = CalculationHistory(
                user_id=user_id,
                calculator_type=calculator_type,
                calculator_name=calculator_name,
                calculator_version=result.get("calculator_version"),
                inputs=inputs,
                result=result["result"],
                formula=result.get("formula"),
                assumptions=result.get("assumptions")
            )
            db.add(history)
            db.commit()
        except Exception as e:
            print(f"Error saving to history: {e}")


@router.post("/sip", response_model=InvestmentResponse)
async def calculate_sip_endpoint(
    request: SIPRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate SIP (Systematic Investment Plan) maturity value"""
    try:
        result = sip.calculate_sip(
            monthly_investment=request.monthly_investment,
            annual_return_rate=request.annual_return_rate,
            tenure_months=request.tenure_months
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "sip", "SIP Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/lumpsum", response_model=InvestmentResponse)
async def calculate_lumpsum_endpoint(
    request: LumpsumRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate lumpsum investment maturity value"""
    try:
        result = sip.calculate_lumpsum(
            principal=request.principal,
            annual_return_rate=request.annual_return_rate,
            tenure_months=request.tenure_months
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "lumpsum", "Lumpsum Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/cagr", response_model=InvestmentResponse)
async def calculate_cagr_endpoint(
    request: CAGRRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate CAGR (Compound Annual Growth Rate)"""
    try:
        result = cagr.calculate_cagr(
            beginning_value=request.beginning_value,
            ending_value=request.ending_value,
            tenure_years=request.tenure_years
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "cagr", "CAGR Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/required-return", response_model=InvestmentResponse)
async def calculate_required_return_endpoint(
    request: RequiredReturnRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate required annual return to achieve target value"""
    try:
        result = cagr.calculate_required_return(
            beginning_value=request.beginning_value,
            target_ending_value=request.target_ending_value,
            tenure_years=request.tenure_years
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "required_return", "Required Return Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/fd", response_model=InvestmentResponse)
async def calculate_fd_endpoint(
    request: FDRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate Fixed Deposit (FD) maturity value"""
    try:
        result = fd.calculate_fd(
            principal=request.principal,
            annual_interest_rate=request.annual_interest_rate,
            tenure_months=request.tenure_months,
            compounding_frequency=request.compounding_frequency
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "fd", "FD Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/rd", response_model=InvestmentResponse)
async def calculate_rd_endpoint(
    request: RDRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate Recurring Deposit (RD) maturity value"""
    try:
        result = rd.calculate_rd(
            monthly_deposit=request.monthly_deposit,
            annual_interest_rate=request.annual_interest_rate,
            tenure_months=request.tenure_months,
            compounding_frequency=request.compounding_frequency
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "rd", "RD Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/rd-simple", response_model=InvestmentResponse)
async def calculate_rd_simple_endpoint(
    request: RDSimpleRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate RD using simplified method"""
    try:
        result = rd.calculate_rd_simple(
            monthly_deposit=request.monthly_deposit,
            annual_interest_rate=request.annual_interest_rate,
            tenure_months=request.tenure_months
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_calculation_to_history(
            db, token if token else None, "rd_simple", "RD Calculator (Simplified)",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
