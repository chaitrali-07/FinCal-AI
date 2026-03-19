"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { getHistory, deleteHistoryRecord } from "@/lib/api";
import { getCalculatorConfig } from "@/lib/calculatorConfig";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Calculator, Trash2, ArrowRight, History,
  AlertCircle, ChevronDown, ChevronUp, Search,
} from "lucide-react";
import { cn } from "@/lib/utils";

// ── Types ─────────────────────────────────────────────────────────────────────
type HistoryRecord = {
  id: string;
  calculator_type: string;
  calculator_name: string;
  inputs: Record<string, number>;
  result: Record<string, unknown>;
  created_at: string;
};

// ── Formatters ────────────────────────────────────────────────────────────────
function formatKey(key: string) {
  return key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
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

function timeAgo(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60)    return "just now";
  if (diff < 3600)  return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

// ── Single history row ────────────────────────────────────────────────────────
function HistoryRow({
  record, onDelete,
}: {
  record: HistoryRecord;
  onDelete: (id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const config = getCalculatorConfig(record.calculator_type);
  const Icon   = config?.icon ?? Calculator;
  const bg     = config?.bgColor ?? "from-emerald-500 to-teal-500";

  const inputEntries  = Object.entries(record.inputs  ?? {});
  const resultEntries = Object.entries(record.result  ?? {}).filter(([k]) => k !== "type" && k !== "status");

  // Pick top 2 result values to show as summary
  const summary = resultEntries.slice(0, 2);

  return (
    <Card className={cn(
      "border-border/60 bg-card/60 backdrop-blur transition-all duration-200",
      expanded ? "border-emerald-500/30 shadow-md" : "hover:border-border"
    )}>
      <CardContent className="p-0">
        {/* ── Row header ── */}
        <div
          className="flex items-center gap-3 p-4 cursor-pointer"
          onClick={() => setExpanded(e => !e)}
        >
          {/* Icon */}
          <div className={cn("flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br shadow-md", bg)}>
            <Icon className="h-5 w-5 text-white" />
          </div>

          {/* Name + time */}
          <div className="flex-1 min-w-0">
            <p className="font-semibold text-sm truncate">{record.calculator_name}</p>
            <p className="text-xs text-muted-foreground">{timeAgo(record.created_at)}</p>
          </div>

          {/* Summary values */}
          <div className="hidden sm:flex gap-4 mr-2">
            {summary.map(([k, v]) => (
              <div key={k} className="text-right">
                <p className="text-[10px] text-muted-foreground">{formatKey(k)}</p>
                <p className="text-sm font-semibold">{formatValue(v)}</p>
              </div>
            ))}
          </div>

          {/* Expand chevron */}
          {expanded
            ? <ChevronUp   className="h-4 w-4 text-muted-foreground shrink-0" />
            : <ChevronDown className="h-4 w-4 text-muted-foreground shrink-0" />}
        </div>

        {/* ── Expanded detail ── */}
        {expanded && (
          <div className="border-t border-border/40 px-4 pb-4 pt-3 space-y-4">

            {/* Inputs */}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Inputs</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {inputEntries.map(([k, v]) => (
                  <div key={k} className="rounded-lg bg-background/50 border border-border/30 px-3 py-2">
                    <p className="text-[10px] text-muted-foreground">{formatKey(k)}</p>
                    <p className="text-sm font-medium">{formatValue(v)}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Results */}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Results</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {resultEntries.map(([k, v]) => (
                  <div key={k} className="rounded-lg bg-emerald-500/5 border border-emerald-500/20 px-3 py-2">
                    <p className="text-[10px] text-muted-foreground">{formatKey(k)}</p>
                    <p className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">{formatValue(v)}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between pt-1">
              <Link href={`/calculators/${record.calculator_type}`}>
                <Button variant="outline" size="sm" className="gap-1.5 text-xs">
                  <ArrowRight className="h-3.5 w-3.5" />
                  Use Again
                </Button>
              </Link>
              <Button
                variant="ghost"
                size="sm"
                className="gap-1.5 text-xs text-destructive hover:text-destructive hover:bg-destructive/10"
                disabled={deleting}
                onClick={async () => {
                  setDeleting(true);
                  onDelete(record.id);
                }}
              >
                <Trash2 className="h-3.5 w-3.5" />
                {deleting ? "Deleting..." : "Delete"}
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// ── Loading skeletons ─────────────────────────────────────────────────────────
function HistorySkeleton() {
  return (
    <div className="space-y-3">
      {[0, 1, 2, 3, 4].map(i => (
        <Card key={i} className="border-border/60 bg-card/60">
          <CardContent className="p-4 flex items-center gap-3">
            <Skeleton className="h-10 w-10 rounded-xl shrink-0" />
            <div className="flex-1 space-y-2">
              <Skeleton className="h-4 w-40" />
              <Skeleton className="h-3 w-24" />
            </div>
            <Skeleton className="h-4 w-20 hidden sm:block" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
function HistoryContent() {
  const { user } = useAuth();
  const [records, setRecords]   = useState<HistoryRecord[]>([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState<string | null>(null);
  const [search, setSearch]     = useState("");
  const [filter, setFilter]     = useState("all");

  useEffect(() => {
    if (!user) return;
    user.getIdToken().then(token =>
      getHistory(token)
        .then(data => setRecords(data.history ?? []))
        .catch(e => setError(e.message))
        .finally(() => setLoading(false))
    );
  }, [user]);

  const handleDelete = async (id: string) => {
    if (!user) return;
    const token = await user.getIdToken();
    try {
      await deleteHistoryRecord(id, token);
      setRecords(prev => prev.filter(r => r.id !== id));
    } catch {
      alert("Failed to delete record");
    }
  };

  // Unique calculator types for filter tabs
  const types = ["all", ...Array.from(new Set(records.map(r => r.calculator_type)))];

  const filtered = records.filter(r => {
    const matchesFilter = filter === "all" || r.calculator_type === filter;
    const matchesSearch = !search ||
      r.calculator_name.toLowerCase().includes(search.toLowerCase()) ||
      r.calculator_type.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="container max-w-4xl mx-auto px-4 sm:px-6 py-12">

      {/* ── Header ── */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-3 py-1 text-sm text-emerald-600 dark:text-emerald-400 mb-4">
          <History className="h-3.5 w-3.5" />
          Your Activity
        </div>
        <h1 className="font-display text-3xl sm:text-4xl font-bold mb-2">Calculation History</h1>
        <p className="text-muted-foreground">
          All your past calculations saved in one place.
          {records.length > 0 && (
            <span className="ml-2 text-emerald-600 dark:text-emerald-400 font-medium">
              {records.length} total
            </span>
          )}
        </p>
      </div>

      {/* ── Search + Filter ── */}
      {!loading && records.length > 0 && (
        <div className="space-y-3 mb-6">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search calculations..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 text-sm rounded-xl border border-border/60 bg-card/60 backdrop-blur focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500/50 transition-all"
            />
          </div>

          {/* Filter tabs */}
          <div className="flex flex-wrap gap-2">
            {types.slice(0, 8).map(t => (
              <button
                key={t}
                onClick={() => setFilter(t)}
                className={cn(
                  "text-xs px-3 py-1.5 rounded-full border transition-all font-medium",
                  filter === t
                    ? "bg-emerald-500 text-white border-emerald-500"
                    : "border-border/60 bg-card/60 text-muted-foreground hover:border-emerald-500/40 hover:text-foreground"
                )}
              >
                {t === "all" ? "All" : getCalculatorConfig(t)?.name ?? t}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Loading ── */}
      {loading && <HistorySkeleton />}

      {/* ── Error ── */}
      {error && (
        <div className="flex items-center gap-3 rounded-2xl border border-destructive/20 bg-destructive/5 p-4 text-destructive">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <div>
            <p className="font-medium">Failed to load history</p>
            <p className="text-sm opacity-80">{error}</p>
          </div>
        </div>
      )}

      {/* ── Empty state ── */}
      {!loading && !error && records.length === 0 && (
        <div className="text-center py-20">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-muted mx-auto mb-4">
            <History className="h-8 w-8 text-muted-foreground/40" />
          </div>
          <h3 className="font-display font-semibold text-lg mb-2">No calculations yet</h3>
          <p className="text-muted-foreground text-sm mb-6">
            Your calculation history will appear here after you use any calculator.
          </p>
          <Link href="/calculators">
            <Button variant="gradient">
              <Calculator className="h-4 w-4" />
              Try a Calculator
            </Button>
          </Link>
        </div>
      )}

      {/* ── No search results ── */}
      {!loading && !error && records.length > 0 && filtered.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          <Search className="h-8 w-8 mx-auto mb-3 opacity-30" />
          <p>No calculations match your search</p>
          <button onClick={() => { setSearch(""); setFilter("all"); }}
            className="text-emerald-600 dark:text-emerald-400 text-sm mt-2 hover:underline">
            Clear filters
          </button>
        </div>
      )}

      {/* ── History list ── */}
      {!loading && !error && filtered.length > 0 && (
        <div className="space-y-3">
          {filtered.map(record => (
            <HistoryRow key={record.id} record={record} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function HistoryPage() {
  return (
    <ProtectedRoute>
      <HistoryContent />
    </ProtectedRoute>
  );
}