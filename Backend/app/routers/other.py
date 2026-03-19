"""
FastAPI routes for other calculators (inflation, retirement).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.schemas.other_schema import (
    InflationAdjustedRequest, FutureValueWithInflationRequest,
    RetirementCorpusRequest, RetirementCorpusWithSavingsRequest, OtherCalculationResponse
)
from app.calculators.other import (
    calculate_inflation_adjusted_value, calculate_future_value_with_inflation,
    calculate_retirement_corpus, calculate_retirement_corpus_with_existing_savings
)
from app.db.database import get_db
from app.db.models import CalculationHistory
from app.services.auth import AuthService

router = APIRouter(prefix="/api/calculate/other", tags=["Other Calculators"])


def save_other_calculation(
    db: Session,
    token: Optional[str],
    calculator_type: str,
    calculator_name: str,
    inputs: Dict[str, Any],
    result: Dict[str, Any]
):
    """Helper to save calculation"""
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


@router.post("/inflation-adjusted", response_model=OtherCalculationResponse)
async def calculate_inflation_adjusted_endpoint(
    request: InflationAdjustedRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate purchasing power loss due to inflation.
    Shows how much value a sum of money loses over time due to inflation.
    """
    try:
        result = calculate_inflation_adjusted_value(
            current_value=request.current_value,
            annual_inflation_rate=request.annual_inflation_rate,
            tenure_years=request.tenure_years
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_other_calculation(
            db, token if token else None, "inflation_adjusted", "Inflation Adjusted Value",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/future-value-inflation", response_model=OtherCalculationResponse)
async def calculate_future_value_inflation_endpoint(
    request: FutureValueWithInflationRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate future investment value accounting for inflation.
    Shows both nominal value and real value (inflation-adjusted).
    """
    try:
        result = calculate_future_value_with_inflation(
            current_value=request.current_value,
            annual_return_rate=request.annual_return_rate,
            annual_inflation_rate=request.annual_inflation_rate,
            tenure_years=request.tenure_years
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_other_calculation(
            db, token if token else None, "future_value_inflation", "Future Value with Inflation",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/retirement-corpus", response_model=OtherCalculationResponse)
async def calculate_retirement_corpus_endpoint(
    request: RetirementCorpusRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate retirement corpus required to maintain current lifestyle.
    
    **Parameters:**
    - monthly_expense: Current monthly living expenses
    - annual_inflation_rate: Expected inflation rate
    - years_in_retirement: How many years you expect to live in retirement
    - annual_return_rate: Expected return on investments
    
    **Returns:**
    - Required corpus to be built before retirement
    - Monthly withdrawal amount during retirement
    """
    try:
        result = calculate_retirement_corpus(
            monthly_expense=request.monthly_expense,
            annual_inflation_rate=request.annual_inflation_rate,
            years_in_retirement=request.years_in_retirement,
            annual_return_rate=request.annual_return_rate
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_other_calculation(
            db, token if token else None, "retirement_corpus", "Retirement Corpus Calculator",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/retirement-corpus-with-savings", response_model=OtherCalculationResponse)
async def calculate_retirement_with_savings_endpoint(
    request: RetirementCorpusWithSavingsRequest,
    http_request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Calculate retirement shortfall/surplus considering existing savings.
    
    **Parameters:**
    - monthly_expense: Current monthly living expenses
    - annual_inflation_rate: Expected inflation
    - years_to_retirement: Years until you retire
    - years_in_retirement: Years you expect to live in retirement
    - existing_savings: Current retirement savings
    - annual_return_before_retirement: Expected return before retirement (typically higher)
    - annual_return_in_retirement: Expected return during retirement (typically lower)
    
    **Returns:**
    - Future value of existing savings at retirement
    - Required corpus for retirement
    - Shortfall (if any) or surplus (if any)
    """
    try:
        result = calculate_retirement_corpus_with_existing_savings(
            monthly_expense=request.monthly_expense,
            annual_inflation_rate=request.annual_inflation_rate,
            years_to_retirement=request.years_to_retirement,
            years_in_retirement=request.years_in_retirement,
            existing_savings=request.existing_savings,
            annual_return_before_retirement=request.annual_return_before_retirement,
            annual_return_in_retirement=request.annual_return_in_retirement
        )
        
        token = http_request.headers.get("Authorization", "").replace("Bearer ", "")
        save_other_calculation(
            db, token if token else None, "retirement_corpus_with_savings",
            "Retirement Corpus with Savings",
            request.model_dump(), result
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/info/retirement")
async def get_retirement_info():
    """Get information about retirement calculators"""
    return {
        "name": "Retirement Planning Calculators",
        "description": "Plan for retirement with corpus and savings analysis",
        "version": "1.0",
        "calculators": {
            "retirement_corpus": {
                "purpose": "Calculate minimum corpus needed for retirement",
                "inputs": ["monthly_expense", "years_in_retirement", "inflation_rate", "return_rate"],
                "useful_for": "First-time retirement planning"
            },
            "retirement_with_savings": {
                "purpose": "Check if current savings are sufficient",
                "inputs": ["monthly_expense", "existing_savings", "years_to_retirement"],
                "useful_for": "Mid-career retirement assessment"
            }
        },
        "assumptions": {
            "inflation": "Assumed constant",
            "returns": "Assumed constant",
            "corpus_depletion": "Fully depleted by end of retirement"
        }
    }
