"""
Miscellaneous financial calculators.
Pure functions for inflation and retirement calculations.
"""

from typing import Dict, Any
from app.utils.constants import CALCULATOR_VERSION, MONTHS_IN_YEAR
from app.utils.validation import validate_principal, validate_rate


def calculate_inflation_adjusted_value(
    current_value: float,
    annual_inflation_rate: float,
    tenure_years: float
) -> Dict[str, Any]:
    """
    Calculate future value adjusted for inflation (purchasing power).
    
    Args:
        current_value: Current value in rupees
        annual_inflation_rate: Annual inflation rate as percentage
        tenure_years: Time period in years
    
    Returns:
        Dictionary with inflation-adjusted value
    """
    if current_value < 0:
        raise ValueError("Value cannot be negative")
    validate_rate(annual_inflation_rate)
    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than 0 years")
    
    # Future value with inflation: FV = PV / (1 + inflation_rate)^tenure
    # This shows how much purchasing power is lost
    
    inflation_decimal = annual_inflation_rate / 100
    purchasing_power = current_value / ((1 + inflation_decimal) ** tenure_years)
    loss_of_value = current_value - purchasing_power
    
    return {
        "result": {
            "current_value": round(current_value, 2),
            "purchasing_power_after_inflation": round(purchasing_power, 2),
            "loss_of_value": round(loss_of_value, 2),
            "effective_loss_percentage": round((loss_of_value / current_value) * 100, 2),
        },
        "assumptions": {
            "inflation_consistency": "assumed constant",
            "measurement": "purchasing power erosion"
        },
        "formula": "Purchasing Power = Current Value / (1 + Inflation Rate)^Years",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "current_value": current_value,
            "annual_inflation_rate": annual_inflation_rate,
            "tenure_years": tenure_years
        }
    }


def calculate_future_value_with_inflation(
    current_value: float,
    annual_return_rate: float,
    annual_inflation_rate: float,
    tenure_years: float
) -> Dict[str, Any]:
    """
    Calculate future value and real returns after accounting for inflation.
    
    Args:
        current_value: Current investment value
        annual_return_rate: Expected annual return as percentage
        annual_inflation_rate: Expected annual inflation as percentage
        tenure_years: Time period in years
    
    Returns:
        Dictionary with nominal and real values
    """
    if current_value < 0:
        raise ValueError("Value cannot be negative")
    validate_rate(annual_return_rate)
    validate_rate(annual_inflation_rate)
    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than 0 years")
    
    # Nominal future value
    return_decimal = annual_return_rate / 100
    nominal_value = current_value * ((1 + return_decimal) ** tenure_years)
    
    # Real value (adjusted for inflation)
    inflation_decimal = annual_inflation_rate / 100
    real_value = nominal_value / ((1 + inflation_decimal) ** tenure_years)
    
    # Real return rate
    real_return_rate = ((annual_return_rate - annual_inflation_rate) / (1 + annual_inflation_rate / 100)) * 100
    
    return {
        "result": {
            "initial_investment": round(current_value, 2),
            "nominal_value": round(nominal_value, 2),
            "real_value": round(real_value, 2),
            "nominal_return": round(nominal_value - current_value, 2),
            "real_return": round(real_value - current_value, 2),
            "real_return_rate": round(real_return_rate, 4),
            "inflation_impact": round(nominal_value - real_value, 2),
        },
        "assumptions": {
            "return_consistency": "assumed constant",
            "inflation_consistency": "assumed constant"
        },
        "formula": "Real Value = Nominal Value / (1 + Inflation)^Years",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "current_value": current_value,
            "annual_return_rate": annual_return_rate,
            "annual_inflation_rate": annual_inflation_rate,
            "tenure_years": tenure_years
        }
    }


def calculate_retirement_corpus(
    monthly_expense: float,
    annual_inflation_rate: float,
    years_in_retirement: int,
    annual_return_rate: float
) -> Dict[str, Any]:
    """
    Calculate corpus required for retirement.
    
    Args:
        monthly_expense: Current monthly expense in rupees
        annual_inflation_rate: Expected annual inflation as percentage
        years_in_retirement: Expected years of retirement (e.g., 25, 30)
        annual_return_rate: Expected annual return on corpus as percentage
    
    Returns:
        Dictionary with required corpus calculation
    """
    if monthly_expense <= 0:
        raise ValueError("Monthly expense must be greater than 0")
    validate_rate(annual_inflation_rate)
    if years_in_retirement <= 0:
        raise ValueError("Years in retirement must be greater than 0")
    validate_rate(annual_return_rate)
    
    # Method: Calculate future corpus needed using future value approach
    # Future annual expense = Current annual expense × (1 + inflation)^years
    # Then calculate PV of annuity for retirement period
    
    annual_expense = monthly_expense * 12
    inflation_decimal = annual_inflation_rate / 100
    return_decimal = annual_return_rate / 100
    
    # Expense at start of retirement (assuming retirement starts in 0 years, or can be adjusted)
    expense_at_retirement = annual_expense * ((1 + inflation_decimal) ** 1)
    
    # Calculate required corpus using annuity formula
    # PV = PMT × [1 - (1 + r)^-n] / r
    if return_decimal == 0:
        required_corpus = expense_at_retirement * years_in_retirement
    else:
        pv_factor = (1 - ((1 + return_decimal) ** -years_in_retirement)) / return_decimal
        required_corpus = expense_at_retirement * pv_factor
    
    return {
        "result": {
            "current_monthly_expense": round(monthly_expense, 2),
            "current_annual_expense": round(annual_expense, 2),
            "expense_at_retirement": round(expense_at_retirement, 2),
            "required_corpus": round(required_corpus, 2),
            "years_in_retirement": years_in_retirement,
            "monthly_withdrawal": round(expense_at_retirement / 12, 2),
        },
        "assumptions": {
            "inflation_consistency": "assumed constant",
            "return_consistency": "assumed constant",
            "life_expectancy": f"{years_in_retirement} years",
            "corpus_depleted": "fully"
        },
        "formula": "Corpus = Annual Expense × [1 - (1 + r)^-n] / r",
        "calculator_version": CALCULATOR_VERSION,
        "note": "This is a simplified calculation. Actual needs may vary based on lifestyle changes, medical expenses, etc.",
        "inputs": {
            "monthly_expense": monthly_expense,
            "annual_inflation_rate": annual_inflation_rate,
            "years_in_retirement": years_in_retirement,
            "annual_return_rate": annual_return_rate
        }
    }


def calculate_retirement_corpus_with_existing_savings(
    monthly_expense: float,
    annual_inflation_rate: float,
    years_to_retirement: int,
    years_in_retirement: int,
    existing_savings: float,
    annual_return_before_retirement: float,
    annual_return_in_retirement: float
) -> Dict[str, Any]:
    """
    Calculate additional corpus needed considering existing savings.
    
    Args:
        monthly_expense: Current monthly expense in rupees
        annual_inflation_rate: Expected annual inflation
        years_to_retirement: Years until retirement
        years_in_retirement: Expected years of retirement
        existing_savings: Current retirement savings
        annual_return_before_retirement: Expected annual return before retirement
        annual_return_in_retirement: Expected annual return during retirement
    
    Returns:
        Dictionary with corpus calculation and shortfall/surplus
    """
    if monthly_expense <= 0:
        raise ValueError("Monthly expense must be greater than 0")
    validate_rate(annual_inflation_rate)
    if years_to_retirement < 0:
        raise ValueError("Years to retirement cannot be negative")
    if years_in_retirement <= 0:
        raise ValueError("Years in retirement must be greater than 0")
    if existing_savings < 0:
        raise ValueError("Existing savings cannot be negative")
    validate_rate(annual_return_before_retirement)
    validate_rate(annual_return_in_retirement)
    
    # Future value of existing savings
    growth_rate = annual_return_before_retirement / 100
    future_savings = existing_savings * ((1 + growth_rate) ** years_to_retirement)
    
    # Required corpus at retirement
    retirement_data = calculate_retirement_corpus(
        monthly_expense,
        annual_inflation_rate,
        years_in_retirement,
        annual_return_in_retirement
    )
    required_corpus = retirement_data["result"]["required_corpus"]
    
    # Shortfall or surplus
    shortfall = max(0, required_corpus - future_savings)
    surplus = max(0, future_savings - required_corpus)
    
    return {
        "result": {
            "existing_savings": round(existing_savings, 2),
            "future_savings_value": round(future_savings, 2),
            "required_corpus": round(required_corpus, 2),
            "shortfall": round(shortfall, 2),
            "surplus": round(surplus, 2),
            "adequacy": "surplus" if surplus > 0 else "shortfall",
        },
        "retirement_details": retirement_data["result"],
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "monthly_expense": monthly_expense,
            "annual_inflation_rate": annual_inflation_rate,
            "years_to_retirement": years_to_retirement,
            "years_in_retirement": years_in_retirement,
            "existing_savings": existing_savings,
            "annual_return_before_retirement": annual_return_before_retirement,
            "annual_return_in_retirement": annual_return_in_retirement
        }
    }
