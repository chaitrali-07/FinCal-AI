"""
FastAPI routes for loan calculators.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.schemas.loan_schema import EMIRequest, EMIForPaymentRequest, EMIResponse
from app.calculators.emi import calculate_emi, calculate_emi_for_payment
from app.db.database import get_db
from app.db.models import CalculationHistory
from app.services.auth import AuthService

router = APIRouter(prefix="/api/calculate/loan", tags=["Loan Calculators"])


@router.post("/emi", response_model=EMIResponse)
async def calculate_emi_endpoint(
    request: EMIRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate EMI (Equated Monthly Installment) for a loan.
    
    **Parameters:**
    - principal: Loan amount (₹1,000 - ₹10,00,00,000)
    - interest_rate: Annual interest rate (0.1% - 30%)
    - tenure_months: Loan duration in months (1 - 600 months)
    
    **Returns:**
    - emi: Monthly installment amount
    - total_payment: Total amount to be paid
    - total_interest: Total interest charged
    - assumptions: Calculation assumptions
    - formula: EMI calculation formula
    """
    try:
        result = calculate_emi(
            principal=request.principal,
            annual_interest_rate=request.interest_rate,
            tenure_months=request.tenure_months
        )
        
        # Save to history if user is authenticated
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            try:
                decoded_token = AuthService.verify_token(token)
                user_id = decoded_token.get("uid")
                
                history = CalculationHistory(
                    user_id=user_id,
                    calculator_type="emi",
                    calculator_name="EMI Calculator",
                    calculator_version=result.get("calculator_version"),
                    inputs=request.model_dump(),
                    result=result["result"],
                    formula=result.get("formula"),
                    assumptions=result.get("assumptions")
                )
                db.add(history)
                db.commit()
            except Exception as e:
                # Log error but don't fail the calculation
                print(f"Error saving to history: {e}")
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )


@router.post("/emi-for-payment", response_model=EMIResponse)
async def calculate_emi_for_payment_endpoint(
    request: EMIForPaymentRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate required tenure for a desired EMI (reverse calculation).
    
    **Parameters:**
    - principal: Loan amount
    - interest_rate: Annual interest rate
    - monthly_emi: Desired monthly EMI amount
    
    **Returns:**
    - Calculated tenure in months
    - Verification of EMI with calculated tenure
    """
    try:
        result = calculate_emi_for_payment(
            principal=request.principal,
            annual_interest_rate=request.interest_rate,
            monthly_emi=request.monthly_emi
        )
        
        # Save to history if user is authenticated
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            try:
                decoded_token = AuthService.verify_token(token)
                user_id = decoded_token.get("uid")
                
                history = CalculationHistory(
                    user_id=user_id,
                    calculator_type="emi_for_payment",
                    calculator_name="EMI for Payment Calculator",
                    calculator_version=result.get("calculator_version"),
                    inputs=request.model_dump(),
                    result=result["result"],
                    formula=result.get("formula"),
                    assumptions=result.get("assumptions")
                )
                db.add(history)
                db.commit()
            except Exception as e:
                print(f"Error saving to history: {e}")
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )


@router.get("/emi/info")
async def get_emi_info():
    """Get information about EMI calculator"""
    return {
        "name": "EMI Calculator",
        "description": "Calculate Equated Monthly Installment for loans",
        "version": "1.0",
        "parameters": {
            "principal": {
                "type": "float",
                "description": "Loan amount in rupees",
                "min": 1000,
                "max": 100000000
            },
            "interest_rate": {
                "type": "float",
                "description": "Annual interest rate as percentage",
                "min": 0.1,
                "max": 30
            },
            "tenure_months": {
                "type": "integer",
                "description": "Loan tenure in months",
                "min": 1,
                "max": 600
            }
        },
        "formula": "EMI = P × r × (1+r)^n / ((1+r)^n − 1)",
        "assumptions": {
            "compounding": "monthly",
            "interest_type": "reducing balance"
        }
    }
