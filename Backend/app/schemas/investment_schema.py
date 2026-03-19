"""
Pydantic schemas for investment calculators.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class SIPRequest(BaseModel):
    """Request schema for SIP calculator"""
    monthly_investment: float = Field(..., ge=1000, le=100000000, description="Monthly SIP amount")
    annual_return_rate: float = Field(..., ge=0.1, le=30, description="Expected annual return as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="SIP tenure in months")


class LumpsumRequest(BaseModel):
    """Request schema for lumpsum investment calculator"""
    principal: float = Field(..., ge=1000, le=100000000, description="Investment amount")
    annual_return_rate: float = Field(..., ge=0.1, le=30, description="Expected annual return as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="Investment tenure in months")


class CAGRRequest(BaseModel):
    """Request schema for CAGR calculator"""
    beginning_value: float = Field(..., gt=0, description="Initial investment amount")
    ending_value: float = Field(..., ge=0, description="Final investment value")
    tenure_years: float = Field(..., gt=0, description="Investment period in years")


class RequiredReturnRequest(BaseModel):
    """Request schema for required return calculator"""
    beginning_value: float = Field(..., gt=0, description="Initial investment amount")
    target_ending_value: float = Field(..., ge=0, description="Target future value")
    tenure_years: float = Field(..., gt=0, description="Investment period in years")


class TenureForCAGRRequest(BaseModel):
    """Request schema for tenure calculation given target CAGR"""
    beginning_value: float = Field(..., gt=0, description="Initial investment amount")
    ending_value: float = Field(..., ge=0, description="Target ending value")
    target_cagr_percentage: float = Field(..., ge=0, description="Target CAGR as percentage")


class FDRequest(BaseModel):
    """Request schema for Fixed Deposit calculator"""
    principal: float = Field(..., ge=1000, le=100000000, description="FD amount in rupees")
    annual_interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="FD tenure in months")
    compounding_frequency: Literal["quarterly", "monthly", "half-yearly", "annually", "daily"] = Field(
        default="quarterly",
        description="Interest compounding frequency"
    )


class FDWithPayoutRequest(BaseModel):
    """Request schema for FD with regular payouts"""
    principal: float = Field(..., ge=1000, le=100000000, description="FD amount in rupees")
    annual_interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="FD tenure in months")
    compounding_frequency: Literal["quarterly", "monthly", "half-yearly", "annually"] = Field(
        default="quarterly",
        description="Interest compounding frequency"
    )
    payout_frequency: Literal["maturity", "quarterly", "monthly", "annually", "half-yearly"] = Field(
        default="maturity",
        description="Interest payout frequency"
    )


class RDRequest(BaseModel):
    """Request schema for Recurring Deposit calculator"""
    monthly_deposit: float = Field(..., ge=1000, le=100000000, description="Monthly RD deposit amount")
    annual_interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="RD tenure in months")
    compounding_frequency: Literal["quarterly", "monthly", "half-yearly", "annually"] = Field(
        default="quarterly",
        description="Interest compounding frequency"
    )


class RDSimpleRequest(BaseModel):
    """Request schema for RD calculator using simplified method"""
    monthly_deposit: float = Field(..., ge=1000, le=100000000, description="Monthly RD deposit amount")
    annual_interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="RD tenure in months")


class RequiredMonthlyDepositRequest(BaseModel):
    """Request schema for calculating required monthly RD deposit"""
    target_amount: float = Field(..., gt=0, description="Target maturity amount")
    annual_interest_rate: float = Field(..., ge=0.1, le=30, description="Annual interest rate as percentage")
    tenure_months: int = Field(..., ge=1, le=600, description="RD tenure in months")


# Generic response schemas
class InvestmentResult(BaseModel):
    """Generic investment calculation result"""
    maturity_value: Optional[float] = None
    principal: Optional[float] = None
    invested_amount: Optional[float] = None
    earnings: Optional[float] = None


class InvestmentResponse(BaseModel):
    """Generic investment response with metadata"""
    result: dict
    assumptions: dict
    formula: str
    calculator_version: str
    inputs: dict
    note: Optional[str] = None
