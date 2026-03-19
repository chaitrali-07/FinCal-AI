"""
Income Tax Calculators (Old & New Regime)
Pure functions for deterministic tax calculations.
Based on Indian income tax slabs (2024-2025).
"""

from typing import Dict, Any
from app.utils.constants import CALCULATOR_VERSION, TAX_REGIME_OLD, TAX_REGIME_NEW


def calculate_tax_old_regime(
    gross_income: float,
    age: int = 60
) -> Dict[str, Any]:
    """
    Calculate income tax using OLD REGIME (pre-2020).
    
    Args:
        gross_income: Annual gross income in rupees
        age: Age of taxpayer (determines standard deduction applicable)
    
    Returns:
        Dictionary with tax breakdown and details
    """
    if gross_income < 0:
        raise ValueError("Gross income cannot be negative")
    
    # Standard deduction (old regime)
    standard_deduction = 50_000
    
    taxable_income = max(0, gross_income - standard_deduction)
    
    # Tax slabs for old regime (2024-25)
    # Senior citizen (≥60): Different slabs
    # General: Standard slabs
    
    if age >= 80:
        senior_limit = 5_00_000
        if taxable_income <= senior_limit:
            tax = 0
        else:
            excess = taxable_income - senior_limit
            if excess <= 5_00_000:
                tax = excess * 0.20
            elif excess <= 10_00_000:
                tax = 1_00_000 + (excess - 5_00_000) * 0.30
            else:
                tax = 1_00_000 + 1_50_000 + (excess - 10_00_000) * 0.31
    
    elif age >= 60:
        senior_limit = 3_00_000
        if taxable_income <= senior_limit:
            tax = 0
        else:
            excess = taxable_income - senior_limit
            if excess <= 5_00_000:
                tax = excess * 0.20
            elif excess <= 10_00_000:
                tax = 1_00_000 + (excess - 5_00_000) * 0.30
            else:
                tax = 1_00_000 + 1_50_000 + (excess - 10_00_000) * 0.31
    
    else:
        # General taxpayers
        if taxable_income <= 2_50_000:
            tax = 0
        elif taxable_income <= 5_00_000:
            tax = (taxable_income - 2_50_000) * 0.05
        elif taxable_income <= 10_00_000:
            tax = 12_500 + (taxable_income - 5_00_000) * 0.20
        else:
            tax = 12_500 + 1_00_000 + (taxable_income - 10_00_000) * 0.30
    
    # Health and education cess (4% on tax)
    cess = tax * 0.04
    total_tax = tax + cess
    
    return {
        "result": {
            "gross_income": round(gross_income, 2),
            "standard_deduction": round(standard_deduction, 2),
            "taxable_income": round(taxable_income, 2),
            "income_tax": round(tax, 2),
            "health_education_cess": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "net_income": round(gross_income - total_tax, 2),
            "effective_tax_rate": round((total_tax / gross_income) * 100, 2) if gross_income > 0 else 0,
        },
        "assumptions": {
            "regime": TAX_REGIME_OLD,
            "age_category": "senior" if age >= 60 else "general",
            "no_deductions": "only standard deduction applied",
            "tax_year": "2024-25"
        },
        "formula": "Tax calculated as per old regime slabs",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "gross_income": gross_income,
            "age": age
        }
    }


def calculate_tax_new_regime(
    gross_income: float,
    age: int = 60
) -> Dict[str, Any]:
    """
    Calculate income tax using NEW REGIME (post-2020).
    
    Args:
        gross_income: Annual gross income in rupees
        age: Age of taxpayer (determines applicable slabs)
    
    Returns:
        Dictionary with tax breakdown and details
    """
    if gross_income < 0:
        raise ValueError("Gross income cannot be negative")
    
    # New regime has no standard deduction
    taxable_income = gross_income
    
    # Tax slabs for new regime (2024-25)
    # Senior citizen (≥60): Different slabs
    # General: Standard slabs
    
    if age >= 80:
        if taxable_income <= 3_00_000:
            tax = 0
        elif taxable_income <= 5_00_000:
            tax = (taxable_income - 3_00_000) * 0.10
        elif taxable_income <= 10_00_000:
            tax = 20_000 + (taxable_income - 5_00_000) * 0.15
        elif taxable_income <= 20_00_000:
            tax = 20_000 + 75_000 + (taxable_income - 10_00_000) * 0.20
        else:
            tax = 20_000 + 75_000 + 2_00_000 + (taxable_income - 20_00_000) * 0.30
    
    elif age >= 60:
        if taxable_income <= 3_00_000:
            tax = 0
        elif taxable_income <= 5_00_000:
            tax = (taxable_income - 3_00_000) * 0.10
        elif taxable_income <= 10_00_000:
            tax = 20_000 + (taxable_income - 5_00_000) * 0.15
        elif taxable_income <= 20_00_000:
            tax = 20_000 + 75_000 + (taxable_income - 10_00_000) * 0.20
        else:
            tax = 20_000 + 75_000 + 2_00_000 + (taxable_income - 20_00_000) * 0.30
    
    else:
        # General taxpayers
        if taxable_income <= 4_00_000:
            tax = 0
        elif taxable_income <= 8_00_000:
            tax = (taxable_income - 4_00_000) * 0.05
        elif taxable_income <= 12_00_000:
            tax = 20_000 + (taxable_income - 8_00_000) * 0.10
        elif taxable_income <= 20_00_000:
            tax = 20_000 + 40_000 + (taxable_income - 12_00_000) * 0.15
        else:
            tax = 20_000 + 40_000 + 1_20_000 + (taxable_income - 20_00_000) * 0.30
    
    # Health and education cess (4% on tax)
    cess = tax * 0.04
    total_tax = tax + cess
    
    return {
        "result": {
            "gross_income": round(gross_income, 2),
            "standard_deduction": 0,
            "taxable_income": round(taxable_income, 2),
            "income_tax": round(tax, 2),
            "health_education_cess": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "net_income": round(gross_income - total_tax, 2),
            "effective_tax_rate": round((total_tax / gross_income) * 100, 2) if gross_income > 0 else 0,
        },
        "assumptions": {
            "regime": TAX_REGIME_NEW,
            "age_category": "senior" if age >= 60 else "general",
            "no_deductions": "new regime doesn't allow standard deduction",
            "tax_year": "2024-25"
        },
        "formula": "Tax calculated as per new regime slabs",
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "gross_income": gross_income,
            "age": age
        }
    }


def compare_tax_regimes(
    gross_income: float,
    age: int = 60
) -> Dict[str, Any]:
    """
    Compare tax liability under both old and new regimes.
    
    Args:
        gross_income: Annual gross income in rupees
        age: Age of taxpayer
    
    Returns:
        Dictionary with comparison of both regimes
    """
    old_result = calculate_tax_old_regime(gross_income, age)
    new_result = calculate_tax_new_regime(gross_income, age)
    
    old_tax = old_result["result"]["total_tax"]
    new_tax = new_result["result"]["total_tax"]
    difference = old_tax - new_tax
    better_regime = "old" if old_tax < new_tax else "new"
    
    return {
        "result": {
            "gross_income": round(gross_income, 2),
            "old_regime_tax": round(old_tax, 2),
            "new_regime_tax": round(new_tax, 2),
            "tax_difference": round(abs(difference), 2),
            "better_regime": better_regime,
            "savings_with_better_regime": round(abs(difference), 2),
        },
        "old_regime_details": old_result["result"],
        "new_regime_details": new_result["result"],
        "calculator_version": CALCULATOR_VERSION,
        "inputs": {
            "gross_income": gross_income,
            "age": age
        }
    }
