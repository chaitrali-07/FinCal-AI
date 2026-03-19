"""
SIP (Systematic Investment Plan) Calculator
Pure function for deterministic investment calculations.
"""

from typing import Dict, Any
from app.utils.constants import COMPOUNDING_MONTHLY, CALCULATOR_VERSION, MONTHS_IN_YEAR
from app.utils.validation import validate_principal, validate_rate, validate_tenure


def calculate_sip(
    monthly_investment: float,
    annual_return_rate: float,
    tenure_months: int
) -> Dict[str, Any]:
    """
    Calculate SIP maturity value and returns.
    
    Args:
        monthly_investment: Monthly SIP amount in rupees
        annual_return_rate: Expected annual return rate as percentage
        tenure_months: SIP tenure in months
    
    Returns:
        Dictionary with maturity value, invested amount, and returns
    """
    # Validation
    validate_principal(monthly_investment)
    validate_rate(annual_return_rate)
    validate_tenure(tenure_months)
    
    # Convert annual rate to monthly rate
    monthly_rate = annual_return_rate / 100 / 12
    
    # SIP Maturity Value Formula:
    # FV = P × [((1 + r)^n - 1) / r] × (1 + r)
    # Where: P = monthly investment, r = monthly rate, n = months
    
    if monthly_rate == 0:
        # If rate is 0, maturity value is simply sum of investments
        maturity_value = monthly_investment * tenure_months
    else:
        fv_factor = (((1 + monthly_rate) ** tenure_months) - 1) / monthly_rate
        maturity_value = monthly_investment * fv_factor * (1 + monthly_rate)
    
    invested_amount = monthly_investment * tenure_months
    earnings = maturity_value - invested_amount
    
    return {
        "result": {
            "maturity_value": round(maturity_value, 2),
            "invested_amount": round(invested_amount, 2),
            "earnings": round(earnings, 2),
            "absolute_return_percentage": round((earnings / invested_amount) * 100, 2) if invested_amount > 0 else 0,
        },
        "assumptions": {
            "compounding_frequency": COMPOUNDING_MONTHLY,
            "investment_frequency": "monthly",
            "rate_consistency": "assumed constant"
        },
        "formula": "FV = P × [((1 + r)^n - 1) / r] × (1 + r)",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "monthly_investment": monthly_investment,
            "annual_return_rate": annual_return_rate,
            "tenure_months": tenure_months
        }
    }


def calculate_lumpsum(
    principal: float,
    annual_return_rate: float,
    tenure_months: int
) -> Dict[str, Any]:
    """
    Calculate lumpsum investment maturity value.
    
    Args:
        principal: One-time investment amount in rupees
        annual_return_rate: Expected annual return rate as percentage
        tenure_months: Investment tenure in months
    
    Returns:
        Dictionary with maturity value, principal, and returns
    """
    validate_principal(principal)
    validate_rate(annual_return_rate)
    validate_tenure(tenure_months)
    
    # Convert annual rate to monthly rate
    monthly_rate = annual_return_rate / 100 / 12
    
    # Compound Interest Formula: A = P(1 + r)^n
    maturity_value = principal * ((1 + monthly_rate) ** tenure_months)
    earnings = maturity_value - principal
    
    return {
        "result": {
            "maturity_value": round(maturity_value, 2),
            "principal": round(principal, 2),
            "earnings": round(earnings, 2),
            "absolute_return_percentage": round((earnings / principal) * 100, 2),
        },
        "assumptions": {
            "compounding_frequency": COMPOUNDING_MONTHLY,
            "reinvestment": "automatic",
            "rate_consistency": "assumed constant"
        },
        "formula": "A = P(1 + r)^n",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "principal": principal,
            "annual_return_rate": annual_return_rate,
            "tenure_months": tenure_months
        }
    }
