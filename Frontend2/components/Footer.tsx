import Link from "next/link";
import { TrendingUp } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border/40 bg-background/50 mt-auto">
      <div className="container max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-gradient-to-br from-emerald-500 to-teal-500">
              <TrendingUp className="h-3 w-3 text-white" />
            </div>
            <span className="font-display font-bold text-sm">Finova</span>
            <span className="text-muted-foreground text-sm">— Your AI Financial Companion</span>
          </div>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <Link href="/calculators" className="hover:text-foreground transition-colors">Calculators</Link>
            <Link href="/assistant" className="hover:text-foreground transition-colors">AI Assistant</Link>
            <span>© {new Date().getFullYear()} Finova</span>
          </div>
        </div>
      </div>
    </footer>
  );
}