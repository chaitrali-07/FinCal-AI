"""
EMI (Equated Monthly Installment) Calculator
Pure function for deterministic loan calculations.
"""

from typing import Dict, Any
from app.utils.constants import COMPOUNDING_MONTHLY, CALCULATOR_VERSION
from app.utils.validation import validate_principal, validate_rate, validate_tenure


def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int
) -> Dict[str, Any]:
    """
    Calculate EMI and related loan details.
    
    Args:
        principal: Loan amount in rupees
        annual_interest_rate: Annual interest rate as percentage (e.g., 9.5 for 9.5%)
        tenure_months: Loan tenure in months
    
    Returns:
        Dictionary with EMI, total payment, total interest, and metadata
    """
    # Validation
    validate_principal(principal)
    validate_rate(annual_interest_rate)
    validate_tenure(tenure_months)
    
    # Convert annual rate to monthly rate
    monthly_rate = annual_interest_rate / 100 / 12
    
    # EMI formula: P × r × (1+r)^n / ((1+r)^n − 1)
    # Where: P = principal, r = monthly rate, n = tenure in months
    
    if monthly_rate == 0:
        # If rate is 0, EMI is simply principal divided by months
        emi = principal / tenure_months
        total_interest = 0.0
    else:
        numerator = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months)
        denominator = ((1 + monthly_rate) ** tenure_months) - 1
        emi = numerator / denominator
        total_interest = (emi * tenure_months) - principal
    
    total_payment = principal + total_interest
    
    return {
        "result": {
            "emi": round(emi, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "principal": round(principal, 2),
        },
        "assumptions": {
            "interest_compounding": COMPOUNDING_MONTHLY,
            "payment_frequency": "monthly",
            "interest_calculation": "reducing balance"
        },
        "formula": "EMI = P × r × (1+r)^n / ((1+r)^n − 1)",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "principal": principal,
            "annual_interest_rate": annual_interest_rate,
            "tenure_months": tenure_months
        }
    }


def calculate_emi_for_payment(
    principal: float,
    annual_interest_rate: float,
    monthly_emi: float
) -> Dict[str, Any]:
    """
    Calculate tenure required for a given EMI.
    Reverse calculation: given principal, rate, and desired EMI, find tenure.
    
    Args:
        principal: Loan amount in rupees
        annual_interest_rate: Annual interest rate as percentage
        monthly_emi: Desired monthly EMI amount
    
    Returns:
        Dictionary with tenure in months and related details
    """
    validate_principal(principal)
    validate_rate(annual_interest_rate)
    
    if monthly_emi <= 0:
        raise ValueError("EMI must be greater than 0")
    
    monthly_rate = annual_interest_rate / 100 / 12
    
    if monthly_rate == 0:
        tenure_months = int(principal / monthly_emi)
    else:
        # Reverse EMI formula to find n
        # n = -log(1 - (P×r/EMI)) / log(1 + r)
        import math
        
        ratio = principal * monthly_rate / monthly_emi
        if ratio >= 1:
            raise ValueError("EMI is too low for given principal and interest rate")
        
        tenure_months = int(-math.log(1 - ratio) / math.log(1 + monthly_rate))
    
    # Validate tenure
    validate_tenure(tenure_months)
    
    # Recalculate with exact tenure to verify
    result = calculate_emi(principal, annual_interest_rate, tenure_months)
    result["note"] = "Tenure calculated to match desired EMI"
    result["calculated_tenure"] = tenure_months
    
    return result
