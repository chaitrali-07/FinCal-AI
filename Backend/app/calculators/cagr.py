"""
CAGR (Compound Annual Growth Rate) Calculator
Pure function for investment return analysis.
"""

from typing import Dict, Any
import math
from app.utils.constants import CALCULATOR_VERSION, MONTHS_IN_YEAR


def calculate_cagr(
    beginning_value: float,
    ending_value: float,
    tenure_years: float
) -> Dict[str, Any]:
    """
    Calculate CAGR for an investment.
    
    Args:
        beginning_value: Initial investment amount
        ending_value: Final investment value
        tenure_years: Investment period in years (can be fractional, e.g., 2.5)
    
    Returns:
        Dictionary with CAGR percentage and analysis
    """
    if beginning_value <= 0:
        raise ValueError("Beginning value must be greater than 0")
    if ending_value < 0:
        raise ValueError("Ending value cannot be negative")
    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than 0 years")
    
    # CAGR Formula: CAGR = (Ending Value / Beginning Value)^(1/n) - 1
    # Where n = number of years
    
    cagr_multiplier = ending_value / beginning_value
    cagr_decimal = (cagr_multiplier ** (1 / tenure_years)) - 1
    cagr_percentage = cagr_decimal * 100
    
    total_return = ending_value - beginning_value
    absolute_return_percentage = (total_return / beginning_value) * 100
    
    return {
        "result": {
            "cagr_percentage": round(cagr_percentage, 4),
            "cagr_decimal": round(cagr_decimal, 6),
            "total_return": round(total_return, 2),
            "absolute_return_percentage": round(absolute_return_percentage, 2),
            "beginning_value": round(beginning_value, 2),
            "ending_value": round(ending_value, 2),
        },
        "assumptions": {
            "compounding": "annual",
            "reinvestment": "automatic"
        },
        "formula": "CAGR = (Ending Value / Beginning Value)^(1/n) - 1",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "beginning_value": beginning_value,
            "ending_value": ending_value,
            "tenure_years": tenure_years
        }
    }


def calculate_required_return(
    beginning_value: float,
    target_ending_value: float,
    tenure_years: float
) -> Dict[str, Any]:
    """
    Calculate required annual return to reach a target value.
    
    Args:
        beginning_value: Initial investment amount
        target_ending_value: Target future value
        tenure_years: Investment period in years
    
    Returns:
        Dictionary with required annual return rate
    """
    if beginning_value <= 0:
        raise ValueError("Beginning value must be greater than 0")
    if target_ending_value < beginning_value:
        raise ValueError("Target ending value must be >= beginning value")
    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than 0 years")
    
    # Required Return = (Target Value / Beginning Value)^(1/n) - 1
    
    required_return_decimal = (target_ending_value / beginning_value) ** (1 / tenure_years) - 1
    required_return_percentage = required_return_decimal * 100
    
    return {
        "result": {
            "required_annual_return_percentage": round(required_return_percentage, 4),
            "required_annual_return_decimal": round(required_return_decimal, 6),
            "beginning_value": round(beginning_value, 2),
            "target_ending_value": round(target_ending_value, 2),
        },
        "assumptions": {
            "compounding": "annual",
            "reinvestment": "automatic"
        },
        "formula": "Required Return = (Target Value / Beginning Value)^(1/n) - 1",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "beginning_value": beginning_value,
            "target_ending_value": target_ending_value,
            "tenure_years": tenure_years
        }
    }


def calculate_tenure_for_cagr(
    beginning_value: float,
    ending_value: float,
    target_cagr_percentage: float
) -> Dict[str, Any]:
    """
    Calculate tenure required to achieve target CAGR.
    
    Args:
        beginning_value: Initial investment amount
        ending_value: Target ending value
        target_cagr_percentage: Target CAGR as percentage
    
    Returns:
        Dictionary with required tenure in years
    """
    if beginning_value <= 0:
        raise ValueError("Beginning value must be greater than 0")
    if ending_value < beginning_value:
        raise ValueError("Ending value must be >= beginning value")
    if target_cagr_percentage < 0:
        raise ValueError("CAGR cannot be negative")
    
    # n = log(Ending Value / Beginning Value) / log(1 + CAGR)
    
    target_cagr_decimal = target_cagr_percentage / 100
    
    if target_cagr_decimal == 0:
        # If CAGR is 0, value doesn't change
        if ending_value == beginning_value:
            return {
                "result": {
                    "tenure_years": 0,
                    "note": "No growth required"
                },
                "inputs": {
                    "beginning_value": beginning_value,
                    "ending_value": ending_value,
                    "target_cagr_percentage": target_cagr_percentage
                }
            }
        else:
            raise ValueError("Cannot achieve non-zero growth with 0% CAGR")
    
    tenure_years = math.log(ending_value / beginning_value) / math.log(1 + target_cagr_decimal)
    
    return {
        "result": {
            "tenure_years": round(tenure_years, 2),
            "tenure_months": round(tenure_years * MONTHS_IN_YEAR, 0),
            "beginning_value": round(beginning_value, 2),
            "ending_value": round(ending_value, 2),
            "target_cagr_percentage": target_cagr_percentage,
        },
        "assumptions": {
            "compounding": "annual"
        },
        "formula": "n = log(Ending Value / Beginning Value) / log(1 + CAGR)",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "beginning_value": beginning_value,
            "ending_value": ending_value,
            "target_cagr_percentage": target_cagr_percentage
        }
    }
