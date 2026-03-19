"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Calculator,
  Bot,
  TrendingUp,
  Shield,
  Zap,
  ArrowRight,
  BarChart3,
  PiggyBank,
  DollarSign,
} from "lucide-react";

const features = [
  {
    icon: Calculator,
    title: "6+ Calculators",
    desc: "EMI, SIP, FD, RD, Tax & ROI calculators built for real-world decisions.",
    color: "from-emerald-500 to-teal-500",
  },
  {
    icon: Bot,
    title: "AI Assistant",
    desc: "Ask anything about finance — get instant, intelligent answers.",
    color: "from-blue-500 to-indigo-500",
  },
  {
    icon: Shield,
    title: "Secure & Private",
    desc: "Firebase authentication ensures your data stays yours.",
    color: "from-violet-500 to-purple-500",
  },
];

const stats = [
  { label: "Calculators", value: "6+", icon: BarChart3 },
  { label: "AI Powered", value: "Yes", icon: Zap },
  { label: "Free to Use", value: "100%", icon: PiggyBank },
  { label: "Dark Mode", value: "✓", icon: DollarSign },
];

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-teal-500/5 rounded-full blur-3xl" />
        </div>

        <div className="container max-w-7xl mx-auto px-4 sm:px-6 pt-20 pb-24 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-4 py-1.5 text-sm text-emerald-600 dark:text-emerald-400 mb-8">
            <Zap className="h-3.5 w-3.5" />
            AI-powered financial planning
          </div>

          <h1 className="font-display text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6">
            Make smarter{" "}
            <span className="bg-gradient-to-r from-emerald-500 to-teal-500 bg-clip-text text-transparent">
              financial
            </span>{" "}
            decisions
          </h1>

          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
            Finova combines powerful financial calculators with an AI assistant
            to help you plan, invest, and grow your wealth with confidence.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="gradient" size="lg" asChild className="text-base">
              <Link href="/calculators">
                <Calculator className="h-5 w-5" />
                Try Calculators
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild className="text-base">
              <Link href="/assistant">
                <Bot className="h-5 w-5" />
                Chat with AI
              </Link>
            </Button>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto">
            {stats.map(({ label, value, icon: Icon }) => (
              <div
                key={label}
                className="rounded-2xl border border-border/60 bg-card/50 backdrop-blur p-4 text-center"
              >
                <Icon className="h-5 w-5 text-emerald-500 mx-auto mb-2" />
                <div className="font-display text-2xl font-bold">{value}</div>
                <div className="text-xs text-muted-foreground mt-1">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container max-w-7xl mx-auto px-4 sm:px-6 pb-24">
        <div className="text-center mb-12">
          <h2 className="font-display text-3xl sm:text-4xl font-bold mb-4">
            Everything you need
          </h2>
          <p className="text-muted-foreground text-lg max-w-xl mx-auto">
            From simple calculations to complex financial planning — all in one place.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map(({ icon: Icon, title, desc, color }) => (
            <Card
              key={title}
              className="group relative overflow-hidden border-border/60 bg-card/50 backdrop-blur hover:border-emerald-500/30 transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/5"
            >
              <CardContent className="p-6">
                <div
                  className={`inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${color} shadow-lg mb-4 transition-transform group-hover:scale-110 duration-300`}
                >
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-display text-xl font-semibold mb-2">{title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container max-w-7xl mx-auto px-4 sm:px-6 pb-24">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-500 to-teal-600 p-8 sm:p-12 text-white text-center">
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-4 left-8 w-32 h-32 rounded-full bg-white blur-2xl" />
            <div className="absolute bottom-4 right-8 w-32 h-32 rounded-full bg-white blur-2xl" />
          </div>
          <div className="relative">
            <TrendingUp className="h-10 w-10 mx-auto mb-4 opacity-90" />
            <h2 className="font-display text-3xl sm:text-4xl font-bold mb-4">
              Start planning your future today
            </h2>
            <p className="text-emerald-50 text-lg mb-8 max-w-xl mx-auto">
              Join thousands of users making better financial decisions with Finova.
            </p>
            <Button
              size="lg"
              className="bg-white text-emerald-600 hover:bg-emerald-50 font-semibold text-base shadow-xl"
              asChild
            >
              <Link href="/register">
                Get Started Free
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
