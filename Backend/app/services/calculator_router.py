"""
Calculator router service - maps calculator names to functions.
"""

from typing import Callable, Dict, Any
from app.calculators import emi, sip, cagr, fd, rd, tax, other


class CalculatorRegistry:
    """Registry to map calculator names to their functions"""
    
    # Map of calculator names to functions
    CALCULATORS: Dict[str, Dict[str, Callable]] = {
        # Loan calculators
        "emi": {
            "function": emi.calculate_emi,
            "description": "Equated Monthly Installment (EMI) Calculator"
        },
        "emi_for_payment": {
            "function": emi.calculate_emi_for_payment,
            "description": "Reverse EMI Calculator (find tenure for given EMI)"
        },
        
        # SIP/Investment calculators
        "sip": {
            "function": sip.calculate_sip,
            "description": "Systematic Investment Plan (SIP) Calculator"
        },
        "lumpsum": {
            "function": sip.calculate_lumpsum,
            "description": "Lumpsum Investment Calculator"
        },
        
        # CAGR calculators
        "cagr": {
            "function": cagr.calculate_cagr,
            "description": "Compound Annual Growth Rate (CAGR) Calculator"
        },
        "required_return": {
            "function": cagr.calculate_required_return,
            "description": "Required Return Calculator"
        },
        "tenure_for_cagr": {
            "function": cagr.calculate_tenure_for_cagr,
            "description": "Tenure for Target CAGR Calculator"
        },
        
        # Fixed Deposit calculators
        "fd": {
            "function": fd.calculate_fd,
            "description": "Fixed Deposit (FD) Calculator"
        },
        "fd_with_payout": {
            "function": fd.calculate_fd_with_interest_payout,
            "description": "FD with Regular Interest Payouts Calculator"
        },
        
        # Recurring Deposit calculators
        "rd": {
            "function": rd.calculate_rd,
            "description": "Recurring Deposit (RD) Calculator"
        },
        "rd_simple": {
            "function": rd.calculate_rd_simple,
            "description": "RD Calculator (Simplified Method)"
        },
        "required_rd_deposit": {
            "function": rd.calculate_required_monthly_deposit,
            "description": "Required Monthly RD Deposit Calculator"
        },
        
        # Tax calculators
        "tax_old_regime": {
            "function": tax.calculate_tax_old_regime,
            "description": "Income Tax Calculator (Old Regime)"
        },
        "tax_new_regime": {
            "function": tax.calculate_tax_new_regime,
            "description": "Income Tax Calculator (New Regime)"
        },
        "tax_comparison": {
            "function": tax.compare_tax_regimes,
            "description": "Tax Regime Comparison"
        },
        
        # Other calculators
        "inflation_adjusted": {
            "function": other.calculate_inflation_adjusted_value,
            "description": "Inflation Adjusted Value Calculator"
        },
        "future_value_with_inflation": {
            "function": other.calculate_future_value_with_inflation,
            "description": "Future Value with Inflation Calculator"
        },
        "retirement_corpus": {
            "function": other.calculate_retirement_corpus,
            "description": "Retirement Corpus Calculator"
        },
        "retirement_corpus_with_savings": {
            "function": other.calculate_retirement_corpus_with_existing_savings,
            "description": "Retirement Corpus with Existing Savings Calculator"
        },
    }
    
    @classmethod
    def get_calculator(cls, calculator_name: str) -> Callable:
        """Get calculator function by name"""
        if calculator_name not in cls.CALCULATORS:
            raise ValueError(
                f"Calculator '{calculator_name}' not found. "
                f"Available calculators: {', '.join(cls.CALCULATORS.keys())}"
            )
        return cls.CALCULATORS[calculator_name]["function"]
    
    @classmethod
    def get_calculator_info(cls, calculator_name: str) -> Dict[str, str]:
        """Get calculator information (description, etc.)"""
        if calculator_name not in cls.CALCULATORS:
            raise ValueError(f"Calculator '{calculator_name}' not found")
        return cls.CALCULATORS[calculator_name]
    
    @classmethod
    def list_calculators(cls) -> Dict[str, str]:
        """List all available calculators with descriptions"""
        return {
            name: info["description"]
            for name, info in cls.CALCULATORS.items()
        }
    
    @classmethod
    def execute_calculator(
        cls,
        calculator_name: str,
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a calculator with given inputs.
        
        Args:
            calculator_name: Name of the calculator to execute
            inputs: Dictionary of input parameters
        
        Returns:
            Calculator result
        """
        try:
            calculator_func = cls.get_calculator(calculator_name)
            result = calculator_func(**inputs)
            return result
        except TypeError as e:
            raise ValueError(f"Invalid parameters for calculator '{calculator_name}': {str(e)}")
