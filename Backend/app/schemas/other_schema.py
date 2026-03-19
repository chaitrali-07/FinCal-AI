"""
Pydantic schemas for other calculators (inflation, retirement).
"""

from pydantic import BaseModel, Field
from typing import Optional


class InflationAdjustedRequest(BaseModel):
    """Request schema for inflation adjustment calculator"""
    current_value: float = Field(..., ge=0, description="Current value in rupees")
    annual_inflation_rate: float = Field(..., ge=0.1, le=30, description="Annual inflation rate as percentage")
    tenure_years: float = Field(..., gt=0, le=100, description="Time period in years")


class FutureValueWithInflationRequest(BaseModel):
    """Request schema for future value with inflation"""
    current_value: float = Field(..., ge=0, description="Current investment value")
    annual_return_rate: float = Field(..., ge=0.1, le=30, description="Expected annual return as percentage")
    annual_inflation_rate: float = Field(..., ge=0.1, le=30, description="Expected annual inflation as percentage")
    tenure_years: float = Field(..., gt=0, le=100, description="Time period in years")


class RetirementCorpusRequest(BaseModel):
    """Request schema for retirement corpus calculation"""
    monthly_expense: float = Field(..., gt=0, description="Current monthly expense in rupees")
    annual_inflation_rate: float = Field(..., ge=0.1, le=30, description="Expected annual inflation as percentage")
    years_in_retirement: int = Field(..., gt=0, le=100, description="Expected years of retirement")
    annual_return_rate: float = Field(..., ge=0.1, le=30, description="Expected annual return as percentage")


class RetirementCorpusWithSavingsRequest(BaseModel):
    """Request schema for retirement corpus with existing savings"""
    monthly_expense: float = Field(..., gt=0, description="Current monthly expense in rupees")
    annual_inflation_rate: float = Field(..., ge=0.1, le=30, description="Expected annual inflation as percentage")
    years_to_retirement: int = Field(..., ge=0, le=100, description="Years until retirement")
    years_in_retirement: int = Field(..., gt=0, le=100, description="Expected years of retirement")
    existing_savings: float = Field(..., ge=0, description="Current retirement savings in rupees")
    annual_return_before_retirement: float = Field(..., ge=0.1, le=30, description="Expected return before retirement")
    annual_return_in_retirement: float = Field(..., ge=0.1, le=30, description="Expected return during retirement")


class RetirementResult(BaseModel):
    """Retirement calculation result"""
    required_corpus: float
    years_in_retirement: int
    monthly_withdrawal: float


class RetirementResponse(BaseModel):
    """Generic retirement response"""
    result: dict
    calculator_version: str
    inputs: dict
    note: Optional[str] = None


class OtherCalculationResponse(BaseModel):
    """Generic response for other calculators"""
    result: dict
    assumptions: dict
    formula: str
    calculator_version: str
    inputs: dict
    note: Optional[str] = None
