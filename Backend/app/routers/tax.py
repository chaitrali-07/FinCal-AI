"""
FastAPI routes for tax calculators.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.schemas.tax_schema import TaxCalculationRequest, TaxComparisonRequest, TaxResponse
from app.calculators.tax import (
    calculate_tax_old_regime, calculate_tax_new_regime, compare_tax_regimes
)
from app.db.database import get_db
from app.db.models import CalculationHistory
from app.services.auth import AuthService

router = APIRouter(prefix="/api/calculate/tax", tags=["Tax Calculators"])


def save_tax_calculation(
    db: Session,
    token: Optional[str],
    calculator_type: str,
    calculator_name: str,
    inputs: Dict[str, Any],
    result: Dict[str, Any]
):
    """Helper to save tax calculation"""
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


@router.post("/old-regime", response_model=TaxResponse)
async def calculate_tax_old_regime_endpoint(
    request: TaxCalculationRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate income tax under OLD REGIME (pre-2020).
    
    **Parameters:**
    - gross_income: Annual gross income (₹0 - ₹10,00,00,000)
    - age: Age of taxpayer for slab determination (default: 60)
    
    **Returns:**
    - Taxable income, tax breakdown, and effective tax rate
    """
    try:
        result = calculate_tax_old_regime(
            gross_income=request.gross_income,
            age=request.age
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_tax_calculation(
            db, token if token else None, "tax_old_regime", "Income Tax (Old Regime)",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/new-regime", response_model=TaxResponse)
async def calculate_tax_new_regime_endpoint(
    request: TaxCalculationRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate income tax under NEW REGIME (post-2020).
    
    **Parameters:**
    - gross_income: Annual gross income
    - age: Age of taxpayer
    
    **Returns:**
    - Taxable income, tax breakdown, and effective tax rate
    - New regime typically offers lower tax rates but no standard deduction
    """
    try:
        result = calculate_tax_new_regime(
            gross_income=request.gross_income,
            age=request.age
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_tax_calculation(
            db, token if token else None, "tax_new_regime", "Income Tax (New Regime)",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/compare-regimes", response_model=TaxResponse)
async def compare_regimes_endpoint(
    request: TaxComparisonRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Compare tax liability under both old and new regimes.
    
    **Parameters:**
    - gross_income: Annual gross income
    - age: Age of taxpayer
    
    **Returns:**
    - Tax under old regime
    - Tax under new regime
    - Which regime is more beneficial and savings amount
    """
    try:
        result = compare_tax_regimes(
            gross_income=request.gross_income,
            age=request.age
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_tax_calculation(
            db, token if token else None, "tax_comparison", "Tax Regime Comparison",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/info/old-regime")
async def get_old_regime_info():
    """Get information about old tax regime"""
    return {
        "name": "Income Tax - Old Regime",
        "description": "Tax calculation under pre-2020 regime with standard deduction",
        "version": "1.0",
        "features": {
            "standard_deduction": "₹50,000 for general taxpayers",
            "senior_citizen_limit": "₹3,00,000 (age 60-79), ₹5,00,000 (age 80+)",
            "allows_deductions": True
        },
        "tax_slabs_general": {
            "0_to_250000": "0%",
            "250000_to_500000": "5%",
            "500000_to_1000000": "20%",
            "above_1000000": "30%"
        }
    }


@router.get("/info/new-regime")
async def get_new_regime_info():
    """Get information about new tax regime"""
    return {
        "name": "Income Tax - New Regime",
        "description": "Tax calculation under post-2020 regime without standard deduction",
        "version": "1.0",
        "features": {
            "standard_deduction": "None",
            "no_section_80c": True,
            "lower_tax_rates": True
        },
        "tax_slabs_general": {
            "0_to_400000": "0%",
            "400000_to_800000": "5%",
            "800000_to_1200000": "10%",
            "1200000_to_2000000": "15%",
            "above_2000000": "30%"
        }
    }
