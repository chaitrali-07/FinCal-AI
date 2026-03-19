"""
Validation utilities for calculator inputs.
"""

from app.utils.constants import (
    MIN_PRINCIPAL, MAX_PRINCIPAL, MIN_RATE, MAX_RATE,
    MIN_TENURE_MONTHS, MAX_TENURE_MONTHS
)


def validate_principal(principal: float) -> None:
    """Validate loan/investment principal amount."""
    if principal < MIN_PRINCIPAL:
        raise ValueError(f"Principal must be at least ₹{MIN_PRINCIPAL:,.0f}")
    if principal > MAX_PRINCIPAL:
        raise ValueError(f"Principal cannot exceed ₹{MAX_PRINCIPAL:,.0f}")


def validate_rate(rate: float) -> None:
    """Validate interest/return rate percentage."""
    if rate < 0:
        raise ValueError("Interest rate cannot be negative")
    if rate > MAX_RATE:
        raise ValueError(f"Interest rate cannot exceed {MAX_RATE}%")


def validate_tenure(months: int) -> None:
    """Validate tenure in months."""
    if months < MIN_TENURE_MONTHS:
        raise ValueError(f"Tenure must be at least {MIN_TENURE_MONTHS} month")
    if months > MAX_TENURE_MONTHS:
        raise ValueError(f"Tenure cannot exceed {MAX_TENURE_MONTHS} months ({MAX_TENURE_MONTHS // 12} years)")


def validate_positive(value: float, field_name: str) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")
