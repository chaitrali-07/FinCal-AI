"""
Comprehensive unit tests for all calculator functions.
"""

import pytest
import math
from app.calculators.emi import calculate_emi, calculate_emi_for_payment
from app.calculators.sip import calculate_sip, calculate_lumpsum
from app.calculators.cagr import calculate_cagr, calculate_required_return, calculate_tenure_for_cagr
from app.calculators.fd import calculate_fd, calculate_fd_with_interest_payout
from app.calculators.rd import calculate_rd, calculate_rd_simple, calculate_required_monthly_deposit
from app.calculators.tax import calculate_tax_old_regime, calculate_tax_new_regime, compare_tax_regimes
from app.calculators.other import (
    calculate_inflation_adjusted_value,
    calculate_future_value_with_inflation,
    calculate_retirement_corpus,
    calculate_retirement_corpus_with_existing_savings
)


class TestEMICalculator:
    def test_emi_basic_calculation(self):
        """Test basic EMI calculation"""
        result = calculate_emi(principal=500000, annual_interest_rate=9.5, tenure_months=60)
        
        assert "result" in result
        assert "emi" in result["result"]
        assert result["result"]["principal"] == 500000
        assert result["result"]["emi"] > 0
        assert result["result"]["total_payment"] > result["result"]["principal"]
    
    def test_emi_zero_interest(self):
        """Test EMI with zero interest rate"""
        result = calculate_emi(principal=600000, annual_interest_rate=0, tenure_months=60)
        
        expected_emi = 600000 / 60
        assert result["result"]["emi"] == expected_emi
        assert result["result"]["total_interest"] == 0
    
    def test_emi_invalid_principal(self):
        """Test EMI with invalid principal"""
        with pytest.raises(ValueError):
            calculate_emi(principal=500, annual_interest_rate=9.5, tenure_months=60)
    
    def test_emi_for_payment(self):
        """Test reverse EMI calculation"""
        result = calculate_emi_for_payment(principal=500000, annual_interest_rate=9.5, monthly_emi=10000)
        
        assert "calculated_tenure" in result
        assert result["calculated_tenure"] > 0


class TestSIPCalculator:
    def test_sip_basic_calculation(self):
        """Test basic SIP calculation"""
        result = calculate_sip(monthly_investment=10000, annual_return_rate=12, tenure_months=120)
        
        assert result["result"]["maturity_value"] > 0
        assert result["result"]["invested_amount"] == 10000 * 120
        assert result["result"]["earnings"] > 0
    
    def test_sip_zero_return(self):
        """Test SIP with zero return"""
        result = calculate_sip(monthly_investment=10000, annual_return_rate=0, tenure_months=60)
        
        assert result["result"]["maturity_value"] == 10000 * 60
        assert result["result"]["earnings"] == 0
    
    def test_lumpsum_calculation(self):
        """Test lumpsum investment calculation"""
        result = calculate_lumpsum(principal=100000, annual_return_rate=12, tenure_months=60)
        
        assert result["result"]["maturity_value"] > result["result"]["principal"]
        assert result["result"]["earnings"] > 0


class TestCAGRCalculator:
    def test_cagr_basic_calculation(self):
        """Test CAGR calculation"""
        result = calculate_cagr(beginning_value=100000, ending_value=200000, tenure_years=10)
        
        assert result["result"]["cagr_percentage"] > 0
        assert result["result"]["cagr_percentage"] < 10
    
    def test_cagr_no_growth(self):
        """Test CAGR with no growth"""
        result = calculate_cagr(beginning_value=100000, ending_value=100000, tenure_years=5)
        
        assert result["result"]["cagr_percentage"] == 0
    
    def test_required_return_calculation(self):
        """Test required return calculation"""
        result = calculate_required_return(beginning_value=100000, target_ending_value=200000, tenure_years=10)
        
        assert result["result"]["required_annual_return_percentage"] > 0
    
    def test_tenure_for_cagr(self):
        """Test tenure calculation for target CAGR"""
        result = calculate_tenure_for_cagr(beginning_value=100000, ending_value=200000, target_cagr_percentage=7.2)
        
        assert result["result"]["tenure_years"] > 0


class TestFDCalculator:
    def test_fd_quarterly_compounding(self):
        """Test FD calculation with quarterly compounding"""
        result = calculate_fd(principal=100000, annual_interest_rate=6.5, tenure_months=60, compounding_frequency="quarterly")
        
        assert result["result"]["maturity_value"] > result["result"]["principal"]
        assert result["result"]["interest_earned"] > 0
    
    def test_fd_monthly_compounding(self):
        """Test FD calculation with monthly compounding"""
        result = calculate_fd(principal=100000, annual_interest_rate=6.5, tenure_months=60, compounding_frequency="monthly")
        
        assert result["result"]["maturity_value"] > 0
    
    def test_fd_with_interest_payout(self):
        """Test FD with regular interest payouts"""
        result = calculate_fd_with_interest_payout(
            principal=100000,
            annual_interest_rate=6.5,
            tenure_months=60,
            payout_frequency="quarterly"
        )
        
        assert result["result"]["interest_per_period"] > 0
        assert result["result"]["number_of_payouts"] > 0


class TestRDCalculator:
    def test_rd_basic_calculation(self):
        """Test RD calculation"""
        result = calculate_rd(monthly_deposit=5000, annual_interest_rate=5.5, tenure_months=60)
        
        assert result["result"]["maturity_value"] > result["result"]["total_deposits"]
        assert result["result"]["interest_earned"] > 0
    
    def test_rd_simple_calculation(self):
        """Test RD with simplified method"""
        result = calculate_rd_simple(monthly_deposit=5000, annual_interest_rate=5.5, tenure_months=60)
        
        assert result["result"]["maturity_value"] > 0
    
    def test_required_monthly_deposit(self):
        """Test calculation of required monthly deposit"""
        result = calculate_required_monthly_deposit(target_amount=500000, annual_interest_rate=5.5, tenure_months=60)
        
        assert "calculated_monthly_deposit" in result


class TestTaxCalculators:
    def test_old_regime_general_taxpayer(self):
        """Test tax calculation under old regime for general taxpayer"""
        result = calculate_tax_old_regime(gross_income=1000000, age=40)
        
        assert result["result"]["taxable_income"] < result["result"]["gross_income"]
        assert result["result"]["total_tax"] >= 0
        assert result["result"]["effective_tax_rate"] >= 0
    
    def test_old_regime_senior_citizen(self):
        """Test tax calculation under old regime for senior citizen"""
        result = calculate_tax_old_regime(gross_income=500000, age=65)
        
        assert result["result"]["taxable_income"] <= result["result"]["gross_income"]
    
    def test_new_regime_calculation(self):
        """Test tax calculation under new regime"""
        result = calculate_tax_new_regime(gross_income=1000000, age=40)
        
        assert result["result"]["standard_deduction"] == 0
        assert result["result"]["taxable_income"] == result["result"]["gross_income"]
        assert result["result"]["total_tax"] >= 0
    
    def test_tax_regime_comparison(self):
        """Test comparison between old and new regimes"""
        result = compare_tax_regimes(gross_income=1500000, age=40)
        
        assert "old_regime_details" in result
        assert "new_regime_details" in result
        assert "better_regime" in result["result"]


class TestOtherCalculators:
    def test_inflation_adjusted_value(self):
        """Test inflation adjustment calculation"""
        result = calculate_inflation_adjusted_value(current_value=100000, annual_inflation_rate=5, tenure_years=10)
        
        assert result["result"]["purchasing_power_after_inflation"] < result["result"]["current_value"]
        assert result["result"]["loss_of_value"] > 0
    
    def test_future_value_with_inflation(self):
        """Test future value calculation with inflation"""
        result = calculate_future_value_with_inflation(
            current_value=100000,
            annual_return_rate=12,
            annual_inflation_rate=5,
            tenure_years=10
        )
        
        assert result["result"]["nominal_value"] > result["result"]["initial_investment"]
        assert result["result"]["real_value"] > 0
    
    def test_retirement_corpus_calculation(self):
        """Test retirement corpus calculation"""
        result = calculate_retirement_corpus(
            monthly_expense=50000,
            annual_inflation_rate=5,
            years_in_retirement=25,
            annual_return_rate=8
        )
        
        assert result["result"]["required_corpus"] > 0
        assert result["result"]["monthly_withdrawal"] > 0
    
    def test_retirement_corpus_with_savings(self):
        """Test retirement corpus with existing savings"""
        result = calculate_retirement_corpus_with_existing_savings(
            monthly_expense=50000,
            annual_inflation_rate=5,
            years_to_retirement=15,
            years_in_retirement=25,
            existing_savings=1000000,
            annual_return_before_retirement=12,
            annual_return_in_retirement=8
        )
        
        assert "future_savings_value" in result["result"]
        assert "required_corpus" in result["result"]


class TestEdgeCases:
    def test_large_values(self):
        """Test calculations with large values"""
        result = calculate_emi(principal=10000000, annual_interest_rate=8.5, tenure_months=360)
        
        assert result["result"]["emi"] > 0
    
    def test_fractional_tenure(self):
        """Test CAGR with fractional tenure"""
        result = calculate_cagr(beginning_value=100000, ending_value=150000, tenure_years=2.5)
        
        assert result["result"]["cagr_percentage"] > 0
    
    def test_minimum_values(self):
        """Test with minimum allowed values"""
        result = calculate_emi(principal=1000, annual_interest_rate=0.1, tenure_months=1)
        
        assert result["result"]["emi"] > 0


class TestInputValidation:
    def test_negative_principal(self):
        """Test that negative principal raises error"""
        with pytest.raises(ValueError):
            calculate_emi(principal=-100000, annual_interest_rate=9.5, tenure_months=60)
    
    def test_negative_rate(self):
        """Test that negative rate raises error"""
        with pytest.raises(ValueError):
            calculate_emi(principal=500000, annual_interest_rate=-5, tenure_months=60)
    
    def test_invalid_tenure(self):
        """Test that invalid tenure raises error"""
        with pytest.raises(ValueError):
            calculate_emi(principal=500000, annual_interest_rate=9.5, tenure_months=0)
    
    def test_negative_income(self):
        """Test that negative income raises error"""
        with pytest.raises(ValueError):
            calculate_tax_old_regime(gross_income=-500000, age=40)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
