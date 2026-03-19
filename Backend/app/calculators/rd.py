"""
Recurring Deposit (RD) Calculator
Pure function for deterministic RD maturity calculations.
"""

from typing import Dict, Any
from app.utils.constants import CALCULATOR_VERSION, MONTHS_IN_YEAR
from app.utils.validation import validate_principal, validate_rate, validate_tenure


def calculate_rd(
    monthly_deposit: float,
    annual_interest_rate: float,
    tenure_months: int,
    compounding_frequency: str = "quarterly"
) -> Dict[str, Any]:
    """
    Calculate RD maturity value and interest earned.
    
    Args:
        monthly_deposit: Monthly RD deposit amount in rupees
        annual_interest_rate: Annual interest rate as percentage
        tenure_months: RD tenure in months
        compounding_frequency: "quarterly", "monthly", "annually", "half-yearly"
    
    Returns:
        Dictionary with maturity value, interest, and details
    """
    validate_principal(monthly_deposit)
    validate_rate(annual_interest_rate)
    validate_tenure(tenure_months)
    
    # RD Formula (with regular deposits and compound interest):
    # A = P × [((1 + r)^n - 1) / r] × (1 + r)
    # Where: P = monthly deposit, r = monthly rate, n = months
    
    # Convert annual rate to monthly rate
    monthly_rate = annual_interest_rate / 100 / 12
    
    if monthly_rate == 0:
        # If rate is 0, maturity value is simply sum of deposits
        maturity_value = monthly_deposit * tenure_months
    else:
        # RD formula with monthly compounding
        fv_factor = (((1 + monthly_rate) ** tenure_months) - 1) / monthly_rate
        maturity_value = monthly_deposit * fv_factor * (1 + monthly_rate)
    
    total_deposits = monthly_deposit * tenure_months
    interest_earned = maturity_value - total_deposits
    
    return {
        "result": {
            "maturity_value": round(maturity_value, 2),
            "total_deposits": round(total_deposits, 2),
            "interest_earned": round(interest_earned, 2),
            "effective_annual_rate": round(((1 + monthly_rate) ** 12 - 1) * 100, 4),
        },
        "assumptions": {
            "compounding_frequency": "monthly",
            "deposit_frequency": "monthly",
            "deposit_timing": "beginning of each month",
            "rate_consistency": "fixed for tenure"
        },
        "formula": "A = P × [((1 + r)^n - 1) / r] × (1 + r)",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "monthly_deposit": monthly_deposit,
            "annual_interest_rate": annual_interest_rate,
            "tenure_months": tenure_months,
            "compounding_frequency": compounding_frequency
        }
    }


def calculate_rd_simple(
    monthly_deposit: float,
    annual_interest_rate: float,
    tenure_months: int
) -> Dict[str, Any]:
    """
    Calculate RD using simplified method (some banks use this).
    Interest = (Monthly Deposit × Tenure × (Tenure + 1) / 2 × Rate) / 12
    
    Args:
        monthly_deposit: Monthly RD deposit amount in rupees
        annual_interest_rate: Annual interest rate as percentage
        tenure_months: RD tenure in months
    
    Returns:
        Dictionary with maturity value using simplified calculation
    """
    validate_principal(monthly_deposit)
    validate_rate(annual_interest_rate)
    validate_tenure(tenure_months)
    
    # Simplified RD Interest Formula
    rate_decimal = annual_interest_rate / 100
    interest_earned = (monthly_deposit * tenure_months * (tenure_months + 1) / 2 * rate_decimal) / 12
    
    total_deposits = monthly_deposit * tenure_months
    maturity_value = total_deposits + interest_earned
    
    return {
        "result": {
            "maturity_value": round(maturity_value, 2),
            "total_deposits": round(total_deposits, 2),
            "interest_earned": round(interest_earned, 2),
        },
        "assumptions": {
            "interest_calculation": "simplified method",
            "compounding": "not applied in simplified method",
            "deposit_frequency": "monthly",
            "rate_consistency": "fixed for tenure"
        },
        "formula": "Interest = (Monthly Deposit × Months × (Months + 1) / 2 × Rate) / 12",
        "calculator_version": CALCULATOR_VERSION,
        "note": "This uses the simplified RD interest calculation method",
        "inputs": {
            "monthly_deposit": monthly_deposit,
            "annual_interest_rate": annual_interest_rate,
            "tenure_months": tenure_months
        }
    }


def calculate_required_monthly_deposit(
    target_amount: float,
    annual_interest_rate: float,
    tenure_months: int
) -> Dict[str, Any]:
    """
    Calculate required monthly deposit to achieve target amount.
    
    Args:
        target_amount: Target maturity amount
        annual_interest_rate: Annual interest rate as percentage
        tenure_months: RD tenure in months
    
    Returns:
        Dictionary with required monthly deposit
    """
    validate_principal(target_amount)
    validate_rate(annual_interest_rate)
    validate_tenure(tenure_months)
    
    # Reverse RD formula: P = A / [((1 + r)^n - 1) / r] × (1 + r)]
    
    monthly_rate = annual_interest_rate / 100 / 12
    
    if monthly_rate == 0:
        monthly_deposit = target_amount / tenure_months
    else:
        fv_factor = (((1 + monthly_rate) ** tenure_months) - 1) / monthly_rate
        monthly_deposit = target_amount / (fv_factor * (1 + monthly_rate))
    
    # Validate the result
    if monthly_deposit < 100:  # Assume minimum RD deposit is ₹100
        raise ValueError(f"Required monthly deposit is ₹{monthly_deposit:.2f}, which is below minimum")
    
    # Verify by calculating maturity with found deposit
    result = calculate_rd(monthly_deposit, annual_interest_rate, tenure_months)
    result["note"] = "Monthly deposit calculated to achieve target maturity value"
    result["calculated_monthly_deposit"] = round(monthly_deposit, 2)
    
    return result
