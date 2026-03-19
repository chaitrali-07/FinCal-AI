"""
Pydantic schemas for loan calculators.
"""

from pydantic import BaseModel, Field
from typing import Optional


class EMIRequest(BaseModel):
    """Request schema for EMI calculator"""
    principal: float = Field(..., ge=1000, le=100000000, description="Loan amount in rupees")
    interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="Loan tenure in months")


class EMIForPaymentRequest(BaseModel):
    """Request schema for reverse EMI calculator"""
    principal: float = Field(..., ge=1000, le=100000000, description="Loan amount in rupees")
    interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    monthly_emi: float = Field(..., gt=0, description="Desired monthly EMI amount")


class EMIResult(BaseModel):
    """Response schema for EMI calculation results"""
    emi: float = Field(..., description="Monthly EMI amount")
    total_payment: float = Field(..., description="Total payment over tenure")
    total_interest: float = Field(..., description="Total interest payable")
    principal: float = Field(..., description="Principal amount")


class EMIResponse(BaseModel):
    """Complete EMI response with metadata"""
    result: EMIResult
    assumptions: dict
    formula: str
    calculator_version: str
    inputs: dict


# Generic response schema for loan calculations
class LoanCalculationResponse(BaseModel):
    """Generic response schema for loan calculations"""
    result: dict
    assumptions: dict
    formula: str
    calculator_version: str
    inputs: dict
    note: Optional[str] = None
