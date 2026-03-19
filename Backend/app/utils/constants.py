"""
Global constants for the finance calculator backend.
"""

# Interest compounding types
COMPOUNDING_MONTHLY = "monthly"
COMPOUNDING_QUARTERLY = "quarterly"
COMPOUNDING_ANNUALLY = "annually"
COMPOUNDING_DAILY = "daily"

# Days in year (for daily compounding)
DAYS_IN_YEAR = 365

# Months in year
MONTHS_IN_YEAR = 12

# Tax regimes
TAX_REGIME_OLD = "old"
TAX_REGIME_NEW = "new"

# Calculator versions
CALCULATOR_VERSION = "1.0"

# Validation constants
MIN_PRINCIPAL = 1000  # Minimum loan/investment amount
MAX_PRINCIPAL = 100_000_000  # Maximum loan/investment amount
MIN_RATE = 0.1  # Minimum interest rate percentage
MAX_RATE = 30.0  # Maximum interest rate percentage
MIN_TENURE_MONTHS = 1
MAX_TENURE_MONTHS = 600  # 50 years

# Rounding precision for financial calculations
CURRENCY_PRECISION = 2  # 2 decimal places for currency
PERCENTAGE_PRECISION = 4  # 4 decimal places for percentages
