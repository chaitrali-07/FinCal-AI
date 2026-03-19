"""
Pydantic schemas for tax calculators.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class TaxCalculationRequest(BaseModel):
    """Request schema for tax calculators"""
    gross_income: float = Field(..., ge=0, le=100000000, description="Annual gross income in rupees")
    age: int = Field(default=60, ge=0, le=150, description="Age of taxpayer")


class TaxComparisonRequest(BaseModel):
    """Request schema for tax regime comparison"""
    gross_income: float = Field(..., ge=0, le=100000000, description="Annual gross income in rupees")
    age: int = Field(default=60, ge=0, le=150, description="Age of taxpayer")


class TaxResult(BaseModel):
    """Tax calculation result"""
    gross_income: float
    taxable_income: float
    income_tax: float
    health_education_cess: float
    total_tax: float
    net_income: float
    effective_tax_rate: float


class TaxResponse(BaseModel):
    """Complete tax response with metadata"""
    result: dict
    assumptions: dict
    formula: str
    calculator_version: str
    inputs: dict
    note: Optional[str] = None


class TaxComparisonResponse(BaseModel):
    """Tax regime comparison response"""
    result: dict
    old_regime_details: dict
    new_regime_details: dict
    calculator_version: str
    inputs: dict
