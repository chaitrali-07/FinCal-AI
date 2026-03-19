"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getCalculators } from "@/lib/api";
import { getCalculatorConfig, calculatorConfigs } from "@/lib/calculatorConfig";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Calculator, ArrowRight, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

type CalculatorsResponse = {
  total: number;
  calculators: Record<string, string>;
};

function CalculatorGrid({ calculators }: { calculators: [string, string][] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      {calculators.map(([type, name]) => {
        const config = getCalculatorConfig(type);
        const Icon = config?.icon ?? Calculator;
        const bg = config?.bgColor ?? "from-emerald-500 to-teal-500";
        const desc = config?.description ?? `Use the ${name} to get accurate results.`;

        return (
          <Link key={type} href={`/calculators/${type}`}>
            <Card className="group h-full cursor-pointer border-border/60 bg-card/60 backdrop-blur hover:border-emerald-500/40 hover:shadow-lg hover:shadow-emerald-500/5 transition-all duration-300">
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div
                    className={cn(
                      "flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br shadow-lg transition-transform group-hover:scale-110 duration-300",
                      bg
                    )}
                  >
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-emerald-500 transition-all group-hover:translate-x-1 duration-200 mt-1" />
                </div>
                <h3 className="font-display text-lg font-semibold mb-1.5">{name}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed line-clamp-2">{desc}</p>
              </CardContent>
            </Card>
          </Link>
        );
      })}
    </div>
  );
}

function LoadingGrid() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      {Array.from({ length: 6 }).map((_, i) => (
        <Card key={i} className="border-border/60 bg-card/60">
          <CardContent className="p-6">
            <div className="flex items-start justify-between mb-4">
              <Skeleton className="h-12 w-12 rounded-2xl" />
            </div>
            <Skeleton className="h-5 w-32 mb-2" />
            <Skeleton className="h-4 w-full mb-1" />
            <Skeleton className="h-4 w-3/4" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function CalculatorsContent() {
  const [data, setData] = useState<CalculatorsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCalculators()
      .then(setData)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  // Remove calculators that don't have a working backend route
  const HIDDEN = [
    "required_monthly_rd_deposit", "required_rd_deposit",
    "fd_with_regular_interest_payouts", "fd_with_payout",
    "tenure_for_target_cagr", "tenure_for_cagr",
    "emi_for_payment", "reverse_emi", "reverse-emi",
  ];

  const entries: [string, string][] = data?.calculators
    ? Object.entries(data.calculators).filter(([type]) => !HIDDEN.includes(type.toLowerCase()))
    : [];

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div className="mb-10">
        <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-3 py-1 text-sm text-emerald-600 dark:text-emerald-400 mb-4">
          <Calculator className="h-3.5 w-3.5" />
          Financial Tools
        </div>
        <h1 className="font-display text-4xl sm:text-5xl font-bold mb-3">
          Calculators
        </h1>
        <p className="text-muted-foreground text-lg max-w-xl">
          Precise tools to help you make informed financial decisions.
          {entries.length > 0 && (
            <span className="ml-2 text-emerald-600 dark:text-emerald-400 font-medium">
              {entries.length} tools available
            </span>
          )}
        </p>
      </div>

      {loading && <LoadingGrid />}

      {error && (
        <div className="flex items-center gap-3 rounded-2xl border border-destructive/20 bg-destructive/5 p-4 text-destructive">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <div>
            <p className="font-medium">Failed to load calculators</p>
            <p className="text-sm opacity-80">{error}</p>
          </div>
        </div>
      )}

      {!loading && !error && entries.length > 0 && (
        <CalculatorGrid calculators={entries} />
      )}

      {!loading && !error && entries.length === 0 && (
        <div className="text-center py-16 text-muted-foreground">
          <Calculator className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No calculators available</p>
        </div>
      )}
    </div>
  );
}

export default function CalculatorsPage() {
  return (
    <ProtectedRoute>
      <CalculatorsContent />
    </ProtectedRoute>
  );
}