"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { calculate } from "@/lib/api";
import { getCalculatorConfig, getDefaultConfig } from "@/lib/calculatorConfig";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, AlertCircle, Loader2, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend,
  LineChart, Line, AreaChart, Area,
} from "recharts";

// ── Formatters ────────────────────────────────────────────────────────────────
function formatKey(key: string): string {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") {
    if (Math.abs(value) > 1000)
      return `₹${value.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
    return value.toLocaleString("en-IN", { maximumFractionDigits: 4 });
  }
  return String(value);
}

function formatINR(v: number) {
  if (v >= 1_00_00_000) return `₹${(v / 1_00_00_000).toFixed(2)}Cr`;
  if (v >= 1_00_000)   return `₹${(v / 1_00_000).toFixed(2)}L`;
  if (v >= 1_000)      return `₹${(v / 1_000).toFixed(1)}K`;
  return `₹${v.toFixed(0)}`;
}

// ── Colour palette ────────────────────────────────────────────────────────────
const COLORS = {
  emerald: "#10b981",
  teal:    "#14b8a6",
  blue:    "#3b82f6",
  indigo:  "#6366f1",
  violet:  "#8b5cf6",
  amber:   "#f59e0b",
  rose:    "#f43f5e",
  cyan:    "#06b6d4",
  orange:  "#f97316",
};

// ── Custom tooltip ────────────────────────────────────────────────────────────
function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-xl border border-border/60 bg-background/95 backdrop-blur p-3 shadow-xl text-sm">
      {label && <p className="font-semibold mb-1 text-foreground">{label}</p>}
      {payload.map((p: any) => (
        <p key={p.name} style={{ color: p.color ?? p.fill }} className="font-medium">
          {p.name}: {typeof p.value === "number" ? formatINR(p.value) : p.value}
        </p>
      ))}
    </div>
  );
}

// ── Chart selector — picks the right chart for each calculator type ───────────
function ResultChart({ type, result, inputs }: {
  type: string;
  result: Record<string, unknown>;
  inputs: Record<string, number>;
}) {
  const t = type.replace(/_/g, "-").toLowerCase();

  // ── EMI — Pie: Principal vs Interest ──────────────────────────────────────
  if (t === "emi") {
    const principal = Number(result["Principal Amount"] ?? inputs.principal ?? 0);
    const interest  = Number(result["Total Interest"] ?? 0);
    if (!principal && !interest) return null;
    const data = [
      { name: "Principal", value: principal },
      { name: "Interest",  value: interest  },
    ];
    return (
      <ChartCard title="Principal vs Interest Breakdown">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={65} outerRadius={100}
              paddingAngle={3} dataKey="value" label={({ name, percent }) =>
                `${name} ${(percent * 100).toFixed(1)}%`
              } labelLine={false}>
              <Cell fill={COLORS.emerald} />
              <Cell fill={COLORS.rose} />
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
        <LegendRow items={[
          { color: COLORS.emerald, label: "Principal", value: formatINR(principal) },
          { color: COLORS.rose,    label: "Interest",  value: formatINR(interest)  },
        ]} />
      </ChartCard>
    );
  }

  // ── SIP — Area chart: year-by-year growth ─────────────────────────────────
  if (t === "sip") {
    const monthly  = Number(inputs.monthly_investment ?? 0);
    const rate     = Number(inputs.rate ?? 0);
    const years    = Number(inputs.tenure ?? 0);
    if (!monthly || !rate || !years) return null;

    const r = rate / 12 / 100;
    const data = Array.from({ length: Math.ceil(years) }, (_, i) => {
      const n = (i + 1) * 12;
      const maturity  = monthly * (((1 + r) ** n - 1) / r) * (1 + r);
      const invested  = monthly * n;
      return { year: `Yr ${i + 1}`, Invested: Math.round(invested), Maturity: Math.round(maturity) };
    });

    return (
      <ChartCard title="Year-by-Year SIP Growth">
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <defs>
              <linearGradient id="gMaturity" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor={COLORS.emerald} stopOpacity={0.3} />
                <stop offset="95%" stopColor={COLORS.emerald} stopOpacity={0.02} />
              </linearGradient>
              <linearGradient id="gInvested" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor={COLORS.blue} stopOpacity={0.3} />
                <stop offset="95%" stopColor={COLORS.blue} stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="year" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Area type="monotone" dataKey="Maturity"  stroke={COLORS.emerald} fill="url(#gMaturity)"  strokeWidth={2} />
            <Area type="monotone" dataKey="Invested"  stroke={COLORS.blue}    fill="url(#gInvested)"  strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </ChartCard>
    );
  }

  // ── LUMPSUM — Line chart: compound growth ─────────────────────────────────
  if (t === "lumpsum") {
    const principal = Number(inputs.principal ?? 0);
    const rate      = Number(inputs.rate ?? 0);
    const years     = Number(inputs.tenure ?? 0);
    if (!principal || !rate || !years) return null;

    const r = rate / 12 / 100;
    const data = Array.from({ length: Math.ceil(years) }, (_, i) => {
      const n = (i + 1) * 12;
      return { year: `Yr ${i + 1}`, Value: Math.round(principal * (1 + r) ** n) };
    });

    return (
      <ChartCard title="Lumpsum Growth Over Time">
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="year" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Line type="monotone" dataKey="Value" stroke={COLORS.indigo} strokeWidth={2.5} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>
    );
  }

  // ── FD — Bar: Principal vs Maturity ───────────────────────────────────────
  if (t === "fd") {
    const principal = Number(result["Principal"] ?? inputs.principal ?? 0);
    const maturity  = Number(result["Maturity Value"] ?? 0);
    const interest  = Number(result["Interest Earned"] ?? 0);
    if (!principal || !maturity) return null;

    const data = [
      { name: "Principal", Amount: principal },
      { name: "Interest",  Amount: interest  },
      { name: "Maturity",  Amount: maturity  },
    ];
    return (
      <ChartCard title="FD Breakdown">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Amount" radius={[6, 6, 0, 0]}>
              <Cell fill={COLORS.blue} />
              <Cell fill={COLORS.amber} />
              <Cell fill={COLORS.emerald} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>
    );
  }

  // ── RD / RD-SIMPLE — Pie: Invested vs Interest ────────────────────────────
  if (t === "rd" || t === "rd-simple") {
    const invested = Number(result["Total Invested"] ?? 0);
    const interest = Number(result["Interest Earned"] ?? 0);
    if (!invested && !interest) return null;
    const data = [
      { name: "Invested", value: invested },
      { name: "Interest", value: interest },
    ];
    return (
      <ChartCard title="RD Breakdown">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={65} outerRadius={100}
              paddingAngle={3} dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
              labelLine={false}>
              <Cell fill={COLORS.rose} />
              <Cell fill={COLORS.amber} />
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
        <LegendRow items={[
          { color: COLORS.rose,  label: "Invested", value: formatINR(invested) },
          { color: COLORS.amber, label: "Interest", value: formatINR(interest) },
        ]} />
      </ChartCard>
    );
  }

  // ── TAX OLD / NEW — Bar: Income breakdown ────────────────────────────────
  if (t === "tax-old" || t === "tax-new" || t === "tax_old_regime" || t === "tax_new_regime") {
    const income    = Number(result["Gross Income"]  ?? inputs.income ?? 0);
    const totalTax  = Number(result["Total Tax"]     ?? 0);
    const inHandPay = income - totalTax;
    if (!income) return null;
    const data = [
      { name: "In-Hand",   Amount: inHandPay },
      { name: "Total Tax", Amount: totalTax  },
    ];
    return (
      <ChartCard title="Income vs Tax Breakdown">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={65} outerRadius={100}
              paddingAngle={3} dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
              labelLine={false}>
              {data.map((_, i) => (
                <Cell key={i} fill={i === 0 ? COLORS.emerald : COLORS.rose} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
        <LegendRow items={[
          { color: COLORS.emerald, label: "In-Hand Pay", value: formatINR(inHandPay) },
          { color: COLORS.rose,    label: "Total Tax",   value: formatINR(totalTax)  },
        ]} />
      </ChartCard>
    );
  }

  // ── TAX COMPARE — Bar: Old vs New regime ─────────────────────────────────
  if (t === "tax-compare" || t === "tax_compare") {
    const oldTax = Number(result["Old Regime Tax"] ?? 0);
    const newTax = Number(result["New Regime Tax"] ?? 0);
    if (!oldTax && !newTax) return null;
    const data = [
      { name: "Old Regime", Tax: oldTax },
      { name: "New Regime", Tax: newTax },
    ];
    return (
      <ChartCard title="Tax Regime Comparison">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Tax" radius={[6, 6, 0, 0]}>
              <Cell fill={COLORS.violet} />
              <Cell fill={COLORS.emerald} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="text-xs text-center text-muted-foreground mt-2">
          {oldTax > newTax
            ? `New regime saves you ${formatINR(oldTax - newTax)}`
            : oldTax < newTax
            ? `Old regime saves you ${formatINR(newTax - oldTax)}`
            : "Both regimes have equal tax"}
        </p>
      </ChartCard>
    );
  }

  // ── ROI — Bar: Initial vs Final, with profit highlight ───────────────────
  if (t === "roi") {
    const initial = Number(result["Initial Investment"] ?? 0);
    const final_v = Number(result["Final Value"]        ?? 0);
    const profit  = Number(result["Profit / Loss"]      ?? 0);
    if (!initial || !final_v) return null;
    const data = [
      { name: "Initial",  Value: initial },
      { name: "Final",    Value: final_v },
    ];
    return (
      <ChartCard title="Investment Growth">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Value" radius={[6, 6, 0, 0]}>
              <Cell fill={COLORS.blue} />
              <Cell fill={profit >= 0 ? COLORS.emerald : COLORS.rose} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="text-xs text-center text-muted-foreground mt-2">
          {profit >= 0
            ? `Profit of ${formatINR(profit)} on your investment`
            : `Loss of ${formatINR(Math.abs(profit))} on your investment`}
        </p>
      </ChartCard>
    );
  }

  // ── CAGR — Line: simulated growth ────────────────────────────────────────
  if (t === "cagr") {
    const begin  = Number(inputs.beginning_value ?? 0);
    const end    = Number(inputs.ending_value    ?? 0);
    const years  = Number(inputs.tenure          ?? 0);
    const cagr   = Number(result["CAGR %"]       ?? 0) / 100;
    if (!begin || !years || !cagr) return null;

    const data = Array.from({ length: Math.ceil(years) + 1 }, (_, i) => ({
      year: `Yr ${i}`,
      Value: Math.round(begin * (1 + cagr) ** i),
    }));

    return (
      <ChartCard title="CAGR Growth Trajectory">
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="year" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Line type="monotone" dataKey="Value" stroke={COLORS.cyan} strokeWidth={2.5} dot={{ fill: COLORS.cyan, r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>
    );
  }

  // ── INFLATION — Pie: Remaining value vs Lost value ───────────────────────
  if (t === "inflation") {
    const current  = Number(result["Current Value"]             ?? 0);
    const adjusted = Number(result["Inflation-Adjusted Value"]  ?? 0);
    const lost     = Number(result["Purchasing Power Loss"]     ?? 0);
    if (!current) return null;
    const data = [
      { name: "Real Value", value: Math.max(0, adjusted) },
      { name: "Lost to Inflation", value: Math.max(0, lost) },
    ];
    return (
      <ChartCard title="Purchasing Power Erosion">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={65} outerRadius={100}
              paddingAngle={3} dataKey="value"
              label={({ name, percent }) => `${(percent * 100).toFixed(1)}%`}
              labelLine={false}>
              <Cell fill={COLORS.emerald} />
              <Cell fill={COLORS.orange} />
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
        <LegendRow items={[
          { color: COLORS.emerald, label: "Real Value",         value: formatINR(adjusted) },
          { color: COLORS.orange,  label: "Lost to Inflation",  value: formatINR(lost)     },
        ]} />
      </ChartCard>
    );
  }

  // ── FUTURE VALUE WITH INFLATION — Bar: Nominal vs Real ───────────────────
  if (t === "future-value-inflation" || t === "future_value_inflation") {
    const nominal = Number(result["Nominal Future Value"] ?? 0);
    const real    = Number(result["Real Future Value"]    ?? 0);
    if (!nominal || !real) return null;
    const data = [
      { name: "Nominal Value", Amount: nominal },
      { name: "Real Value",    Amount: real    },
    ];
    return (
      <ChartCard title="Nominal vs Real Future Value">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Amount" radius={[6, 6, 0, 0]}>
              <Cell fill={COLORS.blue} />
              <Cell fill={COLORS.emerald} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="text-xs text-center text-muted-foreground mt-2">
          Inflation reduces your {formatINR(nominal)} to {formatINR(real)} in today's money
        </p>
      </ChartCard>
    );
  }

  // ── RETIREMENT CORPUS — Pie: corpus needed ───────────────────────────────
  if (t === "retirement-corpus" || t === "retirement_corpus") {
    const corpus    = Number(result["Required Corpus"]   ?? 0);
    const monthly   = Number(result["Monthly Expense Today"] ?? inputs.monthly_expense ?? 0);
    const years     = Number(inputs.years_in_retirement  ?? 0);
    const totalNeeds = monthly * years * 12;
    if (!corpus) return null;
    const data = [
      { name: "Returns Contribution", value: Math.max(0, corpus - totalNeeds) },
      { name: "Direct Expense Need",  value: Math.min(corpus, totalNeeds)     },
    ];
    return (
      <ChartCard title="Retirement Corpus Breakdown">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={65} outerRadius={100}
              paddingAngle={3} dataKey="value"
              label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
              labelLine={false}>
              <Cell fill={COLORS.emerald} />
              <Cell fill={COLORS.indigo} />
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
        <p className="text-xs text-center text-muted-foreground mt-2">
          Total corpus required: {formatINR(corpus)}
        </p>
      </ChartCard>
    );
  }

  // ── RETIREMENT WITH SAVINGS — Bar: Required vs Available ─────────────────
  if (t === "retirement-with-savings" || t === "retirement_with_savings") {
    const required  = Number(result["Required Corpus"]         ?? 0);
    const available = Number(result["Future Value of Savings"] ?? 0);
    if (!required || !available) return null;
    const data = [
      { name: "Required Corpus",  Amount: required  },
      { name: "Your Savings",     Amount: available },
    ];
    const surplus = available - required;
    return (
      <ChartCard title="Corpus Required vs Available">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data} margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatINR} tick={{ fontSize: 11 }} width={60} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Amount" radius={[6, 6, 0, 0]}>
              <Cell fill={COLORS.indigo} />
              <Cell fill={surplus >= 0 ? COLORS.emerald : COLORS.rose} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="text-xs text-center text-muted-foreground mt-2">
          {surplus >= 0
            ? `You have a surplus of ${formatINR(surplus)} 🎉`
            : `You have a shortfall of ${formatINR(Math.abs(surplus))} — consider investing more`}
        </p>
      </ChartCard>
    );
  }

  return null; // No chart for this calculator type
}

// ── Chart wrapper card ────────────────────────────────────────────────────────
function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card className="border-border/60 bg-card/60 backdrop-blur mt-6">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold text-foreground">{title}</CardTitle>
      </CardHeader>
      <CardContent className="pt-0">{children}</CardContent>
    </Card>
  );
}

// ── Legend row below pie charts ───────────────────────────────────────────────
function LegendRow({ items }: { items: { color: string; label: string; value: string }[] }) {
  return (
    <div className="flex justify-center gap-6 mt-3">
      {items.map(({ color, label, value }) => (
        <div key={label} className="flex items-center gap-2 text-sm">
          <span className="h-3 w-3 rounded-full shrink-0" style={{ background: color }} />
          <span className="text-muted-foreground">{label}:</span>
          <span className="font-semibold">{value}</span>
        </div>
      ))}
    </div>
  );
}

// ── Result stat cards ─────────────────────────────────────────────────────────
function ResultCard({ result }: { result: Record<string, unknown> }) {
  const entries = Object.entries(result).filter(([k]) => k !== "type" && k !== "status");
  return (
    <Card className="border-emerald-500/20 bg-emerald-500/5 backdrop-blur">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 text-lg">
          <CheckCircle2 className="h-5 w-5" />
          Results
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {entries.map(([key, val]) => (
            <div key={key} className="rounded-xl bg-background/60 border border-border/40 p-3.5">
              <p className="text-xs text-muted-foreground mb-1">{formatKey(key)}</p>
              <p className="font-display font-semibold text-lg">{formatValue(val)}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
function CalculatorDetailContent() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const rawType = params?.type;
  const type = typeof rawType === "string" ? rawType.toLowerCase() : "";

  const config = type
    ? (getCalculatorConfig(type) ?? getDefaultConfig(type, type.toUpperCase()))
    : null;

  const [values, setValues]   = useState<Record<string, string>>({});
  const [result, setResult]   = useState<Record<string, unknown> | null>(null);
  const [inputs, setInputs]   = useState<Record<string, number>>({});
  const [error, setError]     = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!type || !config) {
    return (
      <div className="container max-w-2xl mx-auto px-4 py-16 text-center">
        <AlertCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
        <h2 className="font-display text-2xl font-bold mb-2">Calculator Not Found</h2>
        <p className="text-muted-foreground mb-6">The calculator type is invalid or missing.</p>
        <Button onClick={() => router.push("/calculators")} variant="outline">
          <ArrowLeft className="h-4 w-4" /> Back to Calculators
        </Button>
      </div>
    );
  }

  const Icon = config.icon;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    const body: Record<string, number> = {};
    for (const field of config.fields) {
      const v = parseFloat(values[field.key] ?? "");
      if (isNaN(v)) {
        setError(`Please enter a valid number for "${field.label}"`);
        setLoading(false);
        return;
      }
      body[field.key] = v;
    }

    try {
      const token = user ? await user.getIdToken(true) : null;
      console.log("TOKEN SENT:", token ? token.substring(0, 20) + "..." : "NULL");
      const res = await calculate(type, body, token);
      setResult(res);
      setInputs(body); // save inputs for chart calculations
      // Track in localStorage for dashboard Recent Activity
      try {
        const prev = JSON.parse(localStorage.getItem("finova_recent_calcs") ?? "[]");
        const updated = [{ type, name: config.name, usedAt: Date.now() }, ...prev].slice(0, 20);
        localStorage.setItem("finova_recent_calcs", JSON.stringify(updated));
      } catch { /* ignore */ }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Calculation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container max-w-2xl mx-auto px-4 sm:px-6 py-12">
      {/* Back */}
      <button
        onClick={() => router.push("/calculators")}
        className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors mb-8 group"
      >
        <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1 duration-200" />
        All Calculators
      </button>

      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <div className={cn("flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br shadow-xl shrink-0", config.bgColor)}>
          <Icon className="h-7 w-7 text-white" />
        </div>
        <div>
          <h1 className="font-display text-2xl sm:text-3xl font-bold">{config.name}</h1>
          <p className="text-muted-foreground text-sm mt-1">{config.description}</p>
        </div>
      </div>

      {/* Form */}
      <Card className="border-border/60 bg-card/60 backdrop-blur mb-6">
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            {config.fields.map((field) => (
              <div key={field.key} className="space-y-2">
                <Label htmlFor={field.key}>{field.label}</Label>
                <div className="relative">
                  {field.unit && (
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground font-mono">
                      {field.unit}
                    </span>
                  )}
                  <Input
                    id={field.key}
                    type="number"
                    step="any"
                    min="0"
                    placeholder={field.placeholder}
                    className={field.unit ? "pr-10" : ""}
                    value={values[field.key] ?? ""}
                    onChange={(e) => setValues((prev) => ({ ...prev, [field.key]: e.target.value }))}
                    required
                  />
                </div>
              </div>
            ))}

            {error && (
              <div className="flex items-start gap-2 rounded-xl bg-destructive/10 border border-destructive/20 px-3 py-2.5 text-sm text-destructive">
                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                {error}
              </div>
            )}

            <Button type="submit" variant="gradient" className="w-full" disabled={loading}>
              {loading ? (
                <><Loader2 className="h-4 w-4 animate-spin" />Calculating...</>
              ) : (
                <><Icon className="h-4 w-4" />Calculate</>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Results + Chart */}
      {result && (
        <>
          <ResultCard result={result} />
          <ResultChart type={type} result={result} inputs={inputs} />
        </>
      )}
    </div>
  );
}

export default function CalculatorDetailPage() {
  return (
    <ProtectedRoute>
      <CalculatorDetailContent />
    </ProtectedRoute>
  );
}