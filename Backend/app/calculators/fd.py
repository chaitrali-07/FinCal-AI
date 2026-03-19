"""
Fixed Deposit (FD) Calculator
Pure function for deterministic FD maturity calculations.
"""

from typing import Dict, Any
from app.utils.constants import CALCULATOR_VERSION, MONTHS_IN_YEAR
from app.utils.validation import validate_principal, validate_rate, validate_tenure


def calculate_fd(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
    compounding_frequency: str = "quarterly"
) -> Dict[str, Any]:
    """
    Calculate FD maturity value and interest earned.
    
    Args:
        principal: FD amount in rupees
        annual_interest_rate: Annual interest rate as percentage
        tenure_months: FD tenure in months
        compounding_frequency: "quarterly", "monthly", "annually", "half-yearly"
    
    Returns:
        Dictionary with maturity value, interest, and details
    """
    validate_principal(principal)
    validate_rate(annual_interest_rate)
    validate_tenure(tenure_months)
    
    # Determine compounding periods per year
    compounding_map = {
        "quarterly": 4,
        "monthly": 12,
        "half-yearly": 2,
        "annually": 1,
        "daily": 365
    }
    
    if compounding_frequency not in compounding_map:
        raise ValueError(f"Invalid compounding frequency: {compounding_frequency}")
    
    n = compounding_map[compounding_frequency]
    
    # Compound Interest Formula: A = P(1 + r/n)^(nt)
    # Where: P = principal, r = annual rate, n = compounding periods per year, t = years
    
    tenure_years = tenure_months / MONTHS_IN_YEAR
    rate_decimal = annual_interest_rate / 100
    
    maturity_value = principal * ((1 + rate_decimal / n) ** (n * tenure_years))
    interest_earned = maturity_value - principal
    
    return {
        "result": {
            "maturity_value": round(maturity_value, 2),
            "principal": round(principal, 2),
            "interest_earned": round(interest_earned, 2),
            "effective_annual_rate": round(((1 + rate_decimal / n) ** n - 1) * 100, 4),
        },
        "assumptions": {
            "compounding_frequency": compounding_frequency,
            "interest_payout": "automatic reinvestment",
            "rate_consistency": "fixed for tenure"
        },
        "formula": "A = P(1 + r/n)^(nt)",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "principal": principal,
            "annual_interest_rate": annual_interest_rate,
            "tenure_months": tenure_months,
            "compounding_frequency": compounding_frequency
        }
    }


def calculate_fd_with_interest_payout(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
    compounding_frequency: str = "quarterly",
    payout_frequency: str = "maturity"
) -> Dict[str, Any]:
    """
    Calculate FD with regular interest payouts (not reinvested).
    
    Args:
        principal: FD amount in rupees
        annual_interest_rate: Annual interest rate as percentage
        tenure_months: FD tenure in months
        compounding_frequency: Frequency of interest compounding
        payout_frequency: "maturity", "quarterly", "monthly", "annually"
    
    Returns:
        Dictionary with maturity value and interest details
    """
    validate_principal(principal)
    validate_rate(annual_interest_rate)
    validate_tenure(tenure_months)
    
    if payout_frequency == "maturity":
        # Regular compound interest
        return calculate_fd(principal, annual_interest_rate, tenure_months, compounding_frequency)
    
    # For regular payouts, interest is paid out periodically without reinvestment
    # Total interest = Principal × Rate × Time
    
    payout_map = {
        "quarterly": 4,
        "monthly": 12,
        "annually": 1,
        "half-yearly": 2
    }
    
    if payout_frequency not in payout_map:
        raise ValueError(f"Invalid payout frequency: {payout_frequency}")
    
    tenure_years = tenure_months / MONTHS_IN_YEAR
    rate_decimal = annual_interest_rate / 100
    
    # Simple interest for each payout period
    total_interest = principal * rate_decimal * tenure_years
    interest_per_period = total_interest / payout_map[payout_frequency]
    
    return {
        "result": {
            "principal": round(principal, 2),
            "total_interest": round(total_interest, 2),
            "interest_per_period": round(interest_per_period, 2),
            "maturity_value": round(principal + total_interest, 2),
            "payout_frequency": payout_frequency,
            "number_of_payouts": payout_map[payout_frequency] * int(tenure_years)
        },
        "assumptions": {
            "interest_calculation": "simple interest for periodic payouts",
            "reinvestment": "none - interest paid out regularly",
            "rate_consistency": "fixed for tenure"
        },
        "formula": "Total Interest = P × r × t; Interest per period = Total Interest / Number of periods",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "principal": principal,
            "annual_interest_rate": annual_interest_rate,
            "tenure_months": tenure_months,
            "compounding_frequency": compounding_frequency,
            "payout_frequency": payout_frequency
        }
    }
