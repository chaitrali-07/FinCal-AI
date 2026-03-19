import {
  Calculator,
  TrendingUp,
  Landmark,
  PiggyBank,
  ReceiptText,
  Percent,
  BarChart2,
  Target,
  TrendingDown,
  Wallet,
  Building2,
  ArrowUpDown,
  Clock,
  Coins,
} from "lucide-react";

export type FieldConfig = {
  key: string;
  label: string;
  placeholder: string;
  unit?: string;
};

export type CalculatorConfig = {
  type: string;
  name: string;
  description: string;
  icon: React.ElementType;
  color: string;
  bgColor: string;
  fields: FieldConfig[];
};

export const calculatorConfigs: Record<string, CalculatorConfig> = {

  // ── LOAN ──────────────────────────────────────────────────────────────────
  emi: {
    type: "emi",
    name: "EMI Calculator",
    description: "Calculate your loan EMI, total interest, and repayment schedule.",
    icon: Calculator,
    color: "text-emerald-600",
    bgColor: "from-emerald-500 to-teal-500",
    fields: [
      { key: "principal",  label: "Loan Amount (₹)",            placeholder: "500000", unit: "₹"  },
      { key: "rate",       label: "Interest Rate (% per annum)", placeholder: "8.5",    unit: "%"  },
      { key: "tenure",     label: "Tenure (months)",             placeholder: "60",     unit: "mo" },
    ],
  },


  // ── INVESTMENT ────────────────────────────────────────────────────────────
  sip: {
    type: "sip",
    name: "SIP Calculator",
    description: "Plan your systematic investments and project future wealth.",
    icon: TrendingUp,
    color: "text-blue-600",
    bgColor: "from-blue-500 to-indigo-500",
    fields: [
      { key: "monthly_investment", label: "Monthly Investment (₹)",  placeholder: "5000", unit: "₹"  },
      { key: "rate",               label: "Expected Return (% p.a.)", placeholder: "12",   unit: "%"  },
      { key: "tenure",             label: "Duration (years)",         placeholder: "10",   unit: "yr" },
    ],
  },

  lumpsum: {
    type: "lumpsum",
    name: "Lumpsum Investment Calculator",
    description: "Calculate maturity value of a one-time investment.",
    icon: Coins,
    color: "text-indigo-600",
    bgColor: "from-indigo-500 to-blue-500",
    fields: [
      { key: "principal", label: "Investment Amount (₹)",   placeholder: "100000", unit: "₹"  },
      { key: "rate",      label: "Expected Return (% p.a.)", placeholder: "12",     unit: "%"  },
      { key: "tenure",    label: "Duration (years)",         placeholder: "10",     unit: "yr" },
    ],
  },

  cagr: {
    type: "cagr",
    name: "CAGR Calculator",
    description: "Calculate the Compound Annual Growth Rate of your investment.",
    icon: BarChart2,
    color: "text-cyan-600",
    bgColor: "from-cyan-500 to-blue-500",
    fields: [
      { key: "beginning_value", label: "Beginning Value (₹)", placeholder: "100000", unit: "₹"  },
      { key: "ending_value",    label: "Ending Value (₹)",    placeholder: "200000", unit: "₹"  },
      { key: "tenure",          label: "Period (years)",       placeholder: "5",      unit: "yr" },
    ],
  },

  "required-return": {
    type: "required-return",
    name: "Required Return Calculator",
    description: "Find the annual return needed to reach your target value.",
    icon: Target,
    color: "text-sky-600",
    bgColor: "from-sky-500 to-cyan-500",
    fields: [
      { key: "beginning_value",      label: "Current Value (₹)", placeholder: "100000", unit: "₹"  },
      { key: "target_ending_value",  label: "Target Value (₹)",  placeholder: "500000", unit: "₹"  },
      { key: "tenure",               label: "Period (years)",     placeholder: "10",     unit: "yr" },
    ],
  },

  fd: {
    type: "fd",
    name: "Fixed Deposit Calculator",
    description: "Calculate maturity amount and interest on your fixed deposits.",
    icon: Landmark,
    color: "text-amber-600",
    bgColor: "from-amber-500 to-orange-500",
    fields: [
      { key: "principal", label: "Principal Amount (₹)",  placeholder: "100000", unit: "₹"  },
      { key: "rate",      label: "Interest Rate (% p.a.)", placeholder: "7",      unit: "%"  },
      { key: "tenure",    label: "Duration (years)",       placeholder: "5",      unit: "yr" },
    ],
  },

  rd: {
    type: "rd",
    name: "Recurring Deposit Calculator",
    description: "Plan your monthly savings and calculate RD maturity value.",
    icon: PiggyBank,
    color: "text-rose-600",
    bgColor: "from-rose-500 to-pink-500",
    fields: [
      { key: "monthly_amount", label: "Monthly Deposit (₹)",    placeholder: "2000", unit: "₹"  },
      { key: "rate",           label: "Interest Rate (% p.a.)",  placeholder: "6.5",  unit: "%"  },
      { key: "tenure",         label: "Duration (months)",       placeholder: "24",   unit: "mo" },
    ],
  },

  "rd-simple": {
    type: "rd-simple",
    name: "RD Calculator (Simplified)",
    description: "Quick RD calculation using the simplified interest method.",
    icon: PiggyBank,
    color: "text-pink-600",
    bgColor: "from-pink-500 to-rose-500",
    fields: [
      { key: "monthly_amount", label: "Monthly Deposit (₹)",   placeholder: "2000", unit: "₹"  },
      { key: "rate",           label: "Interest Rate (% p.a.)", placeholder: "6.5",  unit: "%"  },
      { key: "tenure",         label: "Duration (months)",      placeholder: "24",   unit: "mo" },
    ],
  },

  // ── TAX ───────────────────────────────────────────────────────────────────
  "tax-old": {
    type: "tax-old",
    name: "Income Tax Calculator (Old Regime)",
    description: "Calculate income tax under the old tax regime with deductions.",
    icon: ReceiptText,
    color: "text-violet-600",
    bgColor: "from-violet-500 to-purple-500",
    fields: [
      { key: "income", label: "Annual Income (₹)", placeholder: "1000000", unit: "₹"  },
      { key: "age",    label: "Age (years)",        placeholder: "30",      unit: "yr" },
    ],
  },

  "tax-new": {
    type: "tax-new",
    name: "Income Tax Calculator (New Regime)",
    description: "Calculate income tax under the new tax regime.",
    icon: ReceiptText,
    color: "text-purple-600",
    bgColor: "from-purple-500 to-violet-500",
    fields: [
      { key: "income", label: "Annual Income (₹)", placeholder: "1000000", unit: "₹"  },
      { key: "age",    label: "Age (years)",        placeholder: "30",      unit: "yr" },
    ],
  },

  "tax-compare": {
    type: "tax-compare",
    name: "Tax Regime Comparison",
    description: "Compare old vs new tax regime and find which saves more.",
    icon: ArrowUpDown,
    color: "text-fuchsia-600",
    bgColor: "from-fuchsia-500 to-purple-500",
    fields: [
      { key: "income", label: "Annual Income (₹)", placeholder: "1000000", unit: "₹"  },
      { key: "age",    label: "Age (years)",        placeholder: "30",      unit: "yr" },
    ],
  },

  // ── OTHER ─────────────────────────────────────────────────────────────────
  roi: {
    type: "roi",
    name: "ROI Calculator",
    description: "Measure returns on your investment and compare opportunities.",
    icon: Percent,
    color: "text-cyan-600",
    bgColor: "from-cyan-500 to-teal-500",
    fields: [
      { key: "initial_investment", label: "Initial Investment (₹)", placeholder: "100000", unit: "₹"  },
      { key: "final_value",        label: "Final Value (₹)",        placeholder: "150000", unit: "₹"  },
      { key: "tenure",             label: "Period (years)",          placeholder: "3",      unit: "yr" },
    ],
  },

  inflation: {
    type: "inflation",
    name: "Inflation Adjusted Value Calculator",
    description: "See how inflation erodes the purchasing power of your money.",
    icon: TrendingDown,
    color: "text-orange-600",
    bgColor: "from-orange-500 to-red-500",
    fields: [
      { key: "current_value",       label: "Current Value (₹)",       placeholder: "100000", unit: "₹"  },
      { key: "annual_inflation_rate", label: "Inflation Rate (% p.a.)", placeholder: "6",      unit: "%"  },
      { key: "tenure",              label: "Period (years)",            placeholder: "10",     unit: "yr" },
    ],
  },

  "future-value-inflation": {
    type: "future-value-inflation",
    name: "Future Value with Inflation Calculator",
    description: "Calculate real vs nominal future value accounting for inflation.",
    icon: TrendingUp,
    color: "text-red-600",
    bgColor: "from-red-500 to-orange-500",
    fields: [
      { key: "current_value",         label: "Current Value (₹)",         placeholder: "100000", unit: "₹"  },
      { key: "annual_return_rate",    label: "Annual Return Rate (% p.a.)", placeholder: "12",     unit: "%"  },
      { key: "annual_inflation_rate", label: "Inflation Rate (% p.a.)",    placeholder: "6",      unit: "%"  },
      { key: "tenure",                label: "Period (years)",              placeholder: "10",     unit: "yr" },
    ],
  },

  "retirement-corpus": {
    type: "retirement-corpus",
    name: "Retirement Corpus Calculator",
    description: "Find out how much corpus you need to retire comfortably.",
    icon: Building2,
    color: "text-emerald-600",
    bgColor: "from-emerald-600 to-green-500",
    fields: [
      { key: "monthly_expense",      label: "Monthly Expenses (₹)",       placeholder: "50000", unit: "₹"  },
      { key: "annual_inflation_rate", label: "Inflation Rate (% p.a.)",   placeholder: "6",     unit: "%"  },
      { key: "years_in_retirement",  label: "Years in Retirement",         placeholder: "25",    unit: "yr" },
      { key: "annual_return_rate",   label: "Expected Return (% p.a.)",   placeholder: "8",     unit: "%"  },
    ],
  },

  "retirement-with-savings": {
    type: "retirement-with-savings",
    name: "Retirement Corpus with Existing Savings",
    description: "Check if your current savings are enough to retire on.",
    icon: Wallet,
    color: "text-green-600",
    bgColor: "from-green-500 to-emerald-500",
    fields: [
      { key: "monthly_expense",                label: "Monthly Expenses (₹)",              placeholder: "50000", unit: "₹"  },
      { key: "annual_inflation_rate",          label: "Inflation Rate (% p.a.)",           placeholder: "6",     unit: "%"  },
      { key: "years_to_retirement",            label: "Years to Retirement",               placeholder: "20",    unit: "yr" },
      { key: "years_in_retirement",            label: "Years in Retirement",               placeholder: "25",    unit: "yr" },
      { key: "existing_savings",               label: "Existing Savings (₹)",              placeholder: "500000", unit: "₹" },
      { key: "annual_return_before_retirement", label: "Return Before Retirement (% p.a.)", placeholder: "12",   unit: "%"  },
      { key: "annual_return_in_retirement",    label: "Return During Retirement (% p.a.)", placeholder: "8",    unit: "%"  },
    ],
  },

};

export function getCalculatorConfig(type: string): CalculatorConfig | null {
  if (!type) return null;
  // Normalize: underscores → hyphens, lowercase
  // So "tax_new_regime" → "tax-new", "reverse_emi" → "reverse-emi" etc.
  const normalized = type.toLowerCase().replace(/_/g, "-");
  // Try exact match first, then normalized
  return (
    calculatorConfigs[type.toLowerCase()] ??
    calculatorConfigs[normalized] ??
    // Also try mapping backend snake_case names to frontend keys
    BACKEND_TYPE_MAP[type.toLowerCase()] ??
    BACKEND_TYPE_MAP[normalized] ??
    null
  );
}

// Maps backend snake_case/full names → frontend config keys
const BACKEND_TYPE_MAP: Record<string, CalculatorConfig> = {
  "emi_calculator":                         calculatorConfigs["emi"],
  "reverse-emi-calculator":                 calculatorConfigs["reverse-emi"],
  "reverse_emi":                            calculatorConfigs["reverse-emi"],
  "sip_calculator":                         calculatorConfigs["sip"],
  "lumpsum_investment_calculator":          calculatorConfigs["lumpsum"],
  "lumpsum":                                calculatorConfigs["lumpsum"],
  "compound-annual-growth-rate-(cagr)-calculator": calculatorConfigs["cagr"],
  "cagr_calculator":                        calculatorConfigs["cagr"],
  "required-return-calculator":             calculatorConfigs["required-return"],
  "required_return":                        calculatorConfigs["required-return"],
  "required_return_calculator":             calculatorConfigs["required-return"],
  "fixed-deposit-(fd)-calculator":          calculatorConfigs["fd"],
  "fd_calculator":                          calculatorConfigs["fd"],
  "recurring-deposit-(rd)-calculator":      calculatorConfigs["rd"],
  "rd_calculator":                          calculatorConfigs["rd"],
  "rd-calculator-(simplified-method)":      calculatorConfigs["rd-simple"],
  "rd_simple":                              calculatorConfigs["rd-simple"],
  "rd_calculator_simplified":               calculatorConfigs["rd-simple"],
  "income-tax-calculator-(old-regime)":     calculatorConfigs["tax-old"],
  "tax_old_regime":                         calculatorConfigs["tax-old"],
  "income_tax_old_regime":                  calculatorConfigs["tax-old"],
  "income-tax-calculator-(new-regime)":     calculatorConfigs["tax-new"],
  "tax_new_regime":                         calculatorConfigs["tax-new"],
  "income_tax_new_regime":                  calculatorConfigs["tax-new"],
  "tax-regime-comparison":                  calculatorConfigs["tax-compare"],
  "tax_comparison":                         calculatorConfigs["tax-compare"],
  "compare_tax_regimes":                    calculatorConfigs["tax-compare"],
  "inflation-adjusted-value-calculator":    calculatorConfigs["inflation"],
  "inflation_adjusted":                     calculatorConfigs["inflation"],
  "inflation_adjusted_value":               calculatorConfigs["inflation"],
  "future-value-with-inflation-calculator": calculatorConfigs["future-value-inflation"],
  "future_value_with_inflation":            calculatorConfigs["future-value-inflation"],
  "future_value_inflation":                 calculatorConfigs["future-value-inflation"],
  "retirement-corpus-calculator":           calculatorConfigs["retirement-corpus"],
  "retirement_corpus":                      calculatorConfigs["retirement-corpus"],
  "retirement-corpus-with-existing-savings-calculator": calculatorConfigs["retirement-with-savings"],
  "retirement_corpus_with_savings":         calculatorConfigs["retirement-with-savings"],
  "retirement_with_savings":                calculatorConfigs["retirement-with-savings"],
};

export function getDefaultConfig(type: string, name: string): CalculatorConfig {
  return {
    type,
    name,
    description: `Calculate results for ${name}`,
    icon: Calculator,
    color: "text-emerald-600",
    bgColor: "from-emerald-500 to-teal-500",
    fields: [
      { key: "value1", label: "Value 1", placeholder: "Enter value" },
      { key: "value2", label: "Value 2", placeholder: "Enter value" },
      { key: "value3", label: "Value 3", placeholder: "Enter value" },
    ],
  };
}