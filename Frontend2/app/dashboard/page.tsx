"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { getCalculators, getHealth } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  TrendingUp, Calculator, Bot, ArrowRight, Zap, BarChart3,
  PiggyBank, Landmark, Percent, ReceiptText, Sparkles,
  ChevronRight, Clock, Star, History, LayoutGrid,
} from "lucide-react";
import { cn } from "@/lib/utils";

// ── Types ─────────────────────────────────────────────────────────────────────
type RecentEntry = { type: string; name: string; usedAt: number };
type CalcMeta = {
  type: string; label: string; desc: string;
  icon: React.ElementType; bg: string; popular: boolean;
};

// ── Calculator metadata ───────────────────────────────────────────────────────
const CALC_META: Record<string, CalcMeta> = {
  emi: { type: "emi", label: "EMI Calculator",    desc: "Plan your loan repayments",   icon: Calculator,  bg: "from-emerald-500 to-teal-500",  popular: true  },
  sip: { type: "sip", label: "SIP Calculator",    desc: "Grow wealth systematically",  icon: TrendingUp,  bg: "from-blue-500 to-indigo-500",   popular: true  },
  fd:  { type: "fd",  label: "Fixed Deposit",     desc: "Safe, guaranteed returns",    icon: Landmark,    bg: "from-amber-500 to-orange-500",  popular: false },
  rd:  { type: "rd",  label: "Recurring Deposit", desc: "Save a little every month",   icon: PiggyBank,   bg: "from-rose-500 to-pink-500",     popular: false },
  tax: { type: "tax", label: "Income Tax",         desc: "Estimate your tax liability", icon: ReceiptText, bg: "from-violet-500 to-purple-500", popular: false },
  roi: { type: "roi", label: "ROI Calculator",     desc: "Measure your returns",        icon: Percent,     bg: "from-cyan-500 to-teal-500",     popular: false },
};

const ALL_CALCS = Object.values(CALC_META);

// ── localStorage helpers ──────────────────────────────────────────────────────
function getRecentCalcs(): RecentEntry[] {
  try {
    return JSON.parse(localStorage.getItem("finova_recent_calcs") ?? "[]");
  } catch { return []; }
}

function timeAgo(ts: number): string {
  const diff = Math.floor((Date.now() - ts) / 1000);
  if (diff < 60)    return "just now";
  if (diff < 3600)  return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

// ── Financial tips ────────────────────────────────────────────────────────────
const financialTips = [
  { icon: "💡", title: "Start SIP Early",          body: "₹5,000/month at 12% for 20 years = ~₹50 lakhs. Time is your biggest asset." },
  { icon: "🛡️", title: "Emergency Fund First",     body: "Keep 3–6 months of expenses in liquid funds before investing." },
  { icon: "📊", title: "Diversify Investments",    body: "Spread across equity, debt, and gold for balanced, resilient growth." },
  { icon: "🎯", title: "Clear High-Interest Debt", body: "Credit card debt at 36% p.a. is wealth destruction — pay it off first." },
];

const aiSuggestions = [
  "How much should I invest monthly to retire at 50?",
  "What's the difference between SIP and lump sum?",
  "How do I minimise income tax legally?",
  "Is FD better than RD for short-term goals?",
];

// ── Animated counter ──────────────────────────────────────────────────────────
function AnimatedCount({ value, suffix = "" }: { value: number; suffix?: string }) {
  const [n, setN] = useState(0);
  useEffect(() => {
    if (value === 0) return;
    const steps = 40;
    const inc = value / steps;
    let cur = 0;
    const t = setInterval(() => {
      cur += inc;
      if (cur >= value) { setN(value); clearInterval(t); }
      else setN(Math.floor(cur));
    }, 1000 / steps);
    return () => clearInterval(t);
  }, [value]);
  return <span>{n.toLocaleString("en-IN")}{suffix}</span>;
}

// ── Stat card skeleton ────────────────────────────────────────────────────────
function StatSkeleton() {
  return (
    <Card className="border-border/60 bg-card/60">
      <CardContent className="p-5 space-y-3">
        <div className="flex items-center justify-between">
          <Skeleton className="h-9 w-9 rounded-xl" />
          <Skeleton className="h-5 w-16 rounded-full" />
        </div>
        <Skeleton className="h-7 w-24" />
        <Skeleton className="h-4 w-32" />
      </CardContent>
    </Card>
  );
}

// ── Main dashboard ────────────────────────────────────────────────────────────
function DashboardContent() {
  const { user } = useAuth();
  const [backendStatus, setBackendStatus]   = useState<"checking" | "online" | "offline">("checking");
  const [availableCalcs, setAvailableCalcs] = useState<Record<string, string>>({});
  const [loadingCalcs, setLoadingCalcs]     = useState(true);
  const [recentCalcs, setRecentCalcs]       = useState<RecentEntry[]>([]);

  const firstName = user?.displayName?.split(" ")[0] ?? user?.email?.split("@")[0] ?? "there";
  const hour      = new Date().getHours();
  const greeting  = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  useEffect(() => {
    getHealth()
      .then(() => setBackendStatus("online"))
      .catch(() => setBackendStatus("offline"));

    getCalculators()
      .then((data) => setAvailableCalcs(data?.calculators ?? {}))
      .catch(() => setAvailableCalcs(
        Object.fromEntries(ALL_CALCS.map(c => [c.type, c.label]))
      ))
      .finally(() => setLoadingCalcs(false));

    setRecentCalcs(getRecentCalcs());
  }, []);

  const HIDDEN = [
    "required_monthly_rd_deposit", "required_rd_deposit",
    "fd_with_regular_interest_payouts", "fd_with_payout",
    "tenure_for_target_cagr", "tenure_for_cagr",
    "emi_for_payment", "reverse_emi", "reverse-emi",
  ];
  const calcList   = Object.entries(availableCalcs).filter(([type]) => !HIDDEN.includes(type.toLowerCase()));
  const totalCalcs = calcList.length || 15;
  const recentUnique = Array.from(
    new Map(recentCalcs.map(r => [r.type, r])).values()
  ).slice(0, 4);

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">

      {/* ── Welcome hero ─────────────────────────────────────────────────── */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-600 p-6 sm:p-8 text-white">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute -top-8 -right-8 w-64 h-64 rounded-full bg-white blur-3xl" />
          <div className="absolute -bottom-8 -left-8 w-48 h-48 rounded-full bg-white blur-2xl" />
        </div>
        <div className="absolute inset-0 opacity-5"
          style={{ backgroundImage: "radial-gradient(circle,white 1px,transparent 1px)", backgroundSize: "24px 24px" }}
        />
        <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <Sparkles className="h-4 w-4 opacity-80" />
              <span className="text-emerald-100 text-sm font-medium">{greeting}</span>
              <span className={cn(
                "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
                backendStatus === "online"   && "bg-white/20 text-white",
                backendStatus === "offline"  && "bg-red-500/30 text-red-100",
                backendStatus === "checking" && "bg-white/10 text-white/60",
              )}>
                <span className={cn("h-1.5 w-1.5 rounded-full",
                  backendStatus === "online"   && "bg-emerald-300 animate-pulse",
                  backendStatus === "offline"  && "bg-red-300",
                  backendStatus === "checking" && "bg-white/40 animate-pulse",
                )} />
                {backendStatus === "online"   && "API connected"}
                {backendStatus === "offline"  && "API offline — start FastAPI on :8000"}
                {backendStatus === "checking" && "Checking API…"}
              </span>
            </div>
            <h1 className="font-display text-3xl sm:text-4xl font-bold mb-2">{firstName} 👋</h1>
            <p className="text-emerald-50 text-sm sm:text-base max-w-md">
              Your financial command center. Use our calculators and AI assistant to make smarter money decisions.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 shrink-0">
            <Button className="bg-white text-emerald-600 hover:bg-emerald-50 font-semibold shadow-lg" size="lg" asChild>
              <Link href="/calculators"><Calculator className="h-4 w-4" />Open Calculators</Link>
            </Button>
            <Button className="bg-white/20 hover:bg-white/30 text-white border border-white/30 font-semibold backdrop-blur" size="lg" asChild>
              <Link href="/assistant"><Bot className="h-4 w-4" />AI Assistant</Link>
            </Button>
          </div>
        </div>
      </div>

      {/* ── 2 Stat cards ─────────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-4 max-w-2xl">
        {loadingCalcs ? (
          [0, 1].map(i => <StatSkeleton key={i} />)
        ) : (
          <>
            {/* Recently Used */}
            <Card className="border-border/60 bg-card/60 backdrop-blur overflow-hidden group hover:border-emerald-500/30 hover:shadow-md transition-all duration-300">
              <CardContent className="p-4 sm:p-5">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-md">
                    <History className="h-4 w-4 text-white" />
                  </div>
                  <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                    {recentCalcs.length > 0 ? `${recentCalcs.length} uses` : "None yet"}
                  </span>
                </div>
                <div className="font-display text-2xl font-bold mb-0.5">
                  <AnimatedCount value={recentUnique.length} suffix={recentUnique.length === 1 ? " tool" : " tools"} />
                </div>
                <p className="text-xs text-muted-foreground mb-3">Recently Used</p>
                {recentUnique.length > 0 ? (
                  <div className="flex flex-wrap gap-1">
                    {recentUnique.map(r => (
                      <span key={r.type} className="text-[10px] bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-full px-2 py-0.5 font-medium">
                        {r.name}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-[10px] text-muted-foreground italic">Use a calculator to track activity</p>
                )}
              </CardContent>
            </Card>

            {/* Available Calculators */}
            <Card className="border-border/60 bg-card/60 backdrop-blur overflow-hidden group hover:border-blue-500/30 hover:shadow-md transition-all duration-300">
              <CardContent className="p-4 sm:p-5">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-500 shadow-md">
                    <LayoutGrid className="h-4 w-4 text-white" />
                  </div>
                  <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400">
                    Live
                  </span>
                </div>
                <div className="font-display text-2xl font-bold mb-0.5">
                  <AnimatedCount value={totalCalcs} suffix=" available" />
                </div>
                <p className="text-xs text-muted-foreground mb-3">Calculators</p>
                <div className="flex flex-wrap gap-1">
                  {calcList.slice(0, 6).map(([type]) => (
                    <span key={type} className="text-[10px] bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-full px-2 py-0.5 font-medium uppercase">
                      {type}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>

      {/* ── Two column: Quick Launch + sidebar ───────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Quick Launch */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-display text-xl font-bold flex items-center gap-2">
              <Zap className="h-5 w-5 text-emerald-500" />
              Quick Launch
            </h2>
            <Link href="/calculators" className="text-sm text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1">
              View all <ChevronRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {ALL_CALCS.map(({ type, label, desc, icon: Icon, bg, popular }) => (
              <Link key={type} href={`/calculators/${type}`}>
                <Card className="group cursor-pointer border-border/60 bg-card/60 hover:border-emerald-500/40 hover:shadow-md transition-all duration-200">
                  <CardContent className="p-4 flex items-center gap-3">
                    <div className={cn("flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br shadow-md transition-transform group-hover:scale-110 duration-200", bg)}>
                      <Icon className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="font-semibold text-sm truncate">{label}</p>
                        {popular && (
                          <span className="inline-flex items-center gap-0.5 text-[10px] font-medium bg-amber-500/10 text-amber-600 dark:text-amber-400 px-1.5 py-0.5 rounded-full shrink-0">
                            <Star className="h-2.5 w-2.5" /> Popular
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground">{desc}</p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-emerald-500 group-hover:translate-x-1 transition-all duration-200 shrink-0" />
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">

          {/* Recent Activity */}
          <div className="flex items-center justify-between">
            <h2 className="font-display text-xl font-bold flex items-center gap-2">
              <History className="h-5 w-5 text-emerald-500" />
              Recent Activity
            </h2>
            <Link href="/history" className="text-sm text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1">
              View all <ChevronRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          <Card className="border-border/60 bg-card/60 backdrop-blur">
            <CardContent className="p-4">
              {recentCalcs.length === 0 ? (
                <div className="text-center py-6">
                  <Calculator className="h-8 w-8 text-muted-foreground/30 mx-auto mb-2" />
                  <p className="text-sm text-muted-foreground">No calculators used yet</p>
                  <p className="text-xs text-muted-foreground/60 mt-1">Your history will appear here</p>
                </div>
              ) : (
                <div className="space-y-1">
                  {recentCalcs.slice(0, 5).map((entry, i) => {
                    const meta = CALC_META[entry.type];
                    const Icon = meta?.icon ?? Calculator;
                    return (
                      <Link key={i} href={`/calculators/${entry.type}`}>
                        <div className="group flex items-center gap-3 rounded-xl p-2.5 hover:bg-accent transition-all cursor-pointer">
                          <div className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br", meta?.bg ?? "from-emerald-500 to-teal-500")}>
                            <Icon className="h-4 w-4 text-white" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate">{entry.name}</p>
                            <p className="text-xs text-muted-foreground">{timeAgo(entry.usedAt)}</p>
                          </div>
                          <ArrowRight className="h-3.5 w-3.5 text-muted-foreground group-hover:text-emerald-500 group-hover:translate-x-0.5 transition-all shrink-0" />
                        </div>
                      </Link>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Ask AI */}
          <h2 className="font-display text-xl font-bold flex items-center gap-2">
            <Bot className="h-5 w-5 text-blue-500" />
            Ask AI
          </h2>
          <Card className="border-border/60 bg-card/60 backdrop-blur">
            <CardContent className="p-4 space-y-1.5">
              {aiSuggestions.map((q) => (
                <Link key={q} href="/assistant">
                  <div className="group flex items-start gap-2 rounded-xl p-2.5 hover:bg-accent transition-all cursor-pointer">
                    <Sparkles className="h-3.5 w-3.5 text-blue-500 mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground group-hover:text-foreground transition-colors leading-snug">{q}</p>
                  </div>
                </Link>
              ))}
              <div className="pt-2">
                <Button variant="gradient" size="sm" className="w-full" asChild>
                  <Link href="/assistant"><Bot className="h-4 w-4" />Open AI Assistant</Link>
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Profile card */}
          <Card className="border-border/60 bg-card/60 backdrop-blur overflow-hidden">
            <div className="h-1.5 bg-gradient-to-r from-emerald-500 to-teal-500" />
            <CardContent className="p-4">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 text-white font-bold text-sm shadow-md">
                  {firstName[0]?.toUpperCase() ?? "U"}
                </div>
                <div>
                  <p className="font-semibold text-sm">{user?.displayName ?? firstName}</p>
                  <p className="text-xs text-muted-foreground truncate max-w-[160px]">{user?.email}</p>
                </div>
              </div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Clock className="h-3.5 w-3.5" />
                Member since {user?.metadata?.creationTime
                  ? new Date(user.metadata.creationTime).toLocaleDateString("en-IN", { month: "short", year: "numeric" })
                  : "recently"}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* ── Financial tips ────────────────────────────────────────────────── */}
      <div>
        <h2 className="font-display text-xl font-bold flex items-center gap-2 mb-4">
          <BarChart3 className="h-5 w-5 text-violet-500" />
          Financial Wisdom
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {financialTips.map(({ icon, title, body }) => (
            <Card key={title} className="border-border/60 bg-card/60 backdrop-blur hover:border-violet-500/30 transition-all duration-200 group">
              <CardContent className="p-5">
                <span className="text-2xl mb-3 block">{icon}</span>
                <h3 className="font-display font-semibold text-sm mb-1.5 group-hover:text-violet-600 dark:group-hover:text-violet-400 transition-colors">{title}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">{body}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* ── CTA ──────────────────────────────────────────────────────────── */}
      <Card className="border-border/60 bg-card/60 backdrop-blur overflow-hidden">
        <CardContent className="p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-lg shrink-0">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-display font-bold text-lg">Ready to plan your finances?</h3>
                <p className="text-sm text-muted-foreground">Choose a calculator or ask our AI anything about money.</p>
              </div>
            </div>
            <div className="flex gap-3 shrink-0">
              <Button variant="outline" asChild>
                <Link href="/calculators"><Calculator className="h-4 w-4" />Calculators</Link>
              </Button>
              <Button variant="gradient" asChild>
                <Link href="/assistant"><Sparkles className="h-4 w-4" />Ask AI</Link>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}