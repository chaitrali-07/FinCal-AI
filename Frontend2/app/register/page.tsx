"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  createUserWithEmailAndPassword,
  updateProfile,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
} from "firebase/auth";
import { auth, googleProvider } from "@/lib/firebase";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { TrendingUp, Mail, Lock, User, AlertCircle, Eye, EyeOff, Loader2 } from "lucide-react";

function GoogleIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
    </svg>
  );
}

function getFriendlyError(error: unknown): string {
  if (!(error instanceof Error)) return "Something went wrong. Please try again.";
  const msg = error.message;
  if (msg.includes("auth/email-already-in-use"))
    return "An account with this email already exists. Try signing in instead.";
  if (msg.includes("auth/weak-password"))
    return "Password must be at least 6 characters.";
  if (msg.includes("auth/invalid-email"))
    return "Please enter a valid email address.";
  if (msg.includes("auth/too-many-requests"))
    return "Too many attempts. Please wait a few minutes and try again.";
  if (msg.includes("auth/popup-closed-by-user") || msg.includes("auth/cancelled-popup-request"))
    return "";
  if (msg.includes("auth/popup-blocked"))
    return "Popup blocked — falling back to redirect sign-in...";
  if (msg.includes("auth/network-request-failed"))
    return "Network error. Please check your internet connection.";
  if (msg.includes("auth/configuration-not-found") || msg.includes("auth/invalid-api-key"))
    return "Firebase is not configured correctly. Check your .env.local file.";
  if (msg.includes("auth/operation-not-allowed"))
    return "Google sign-in is not enabled. Go to Firebase Console → Authentication → Sign-in method → Enable Google.";
  if (msg.includes("auth/unauthorized-domain"))
    return "This domain is not authorized. Add 'localhost' in Firebase Console → Authentication → Settings → Authorized domains.";
  return msg.replace("Firebase: ", "").replace(/\s*\(auth\/[^)]+\)\.?/, "").trim() || "Registration failed. Please try again.";
}

export default function RegisterPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [checkingRedirect, setCheckingRedirect] = useState(true);

  // Handle returning from Google redirect sign-in
  useEffect(() => {
    getRedirectResult(auth)
      .then((result) => {
        if (result?.user) {
          router.replace("/dashboard");
        }
      })
      .catch((err) => {
        const msg = getFriendlyError(err);
        if (msg) setError(msg);
      })
      .finally(() => setCheckingRedirect(false));
  }, [router]);

  useEffect(() => {
    if (!authLoading && user) {
      router.replace("/dashboard");
    }
  }, [user, authLoading, router]);

  const isInitializing = authLoading || checkingRedirect;

  if (isInitializing) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-lg">
            <TrendingUp className="h-6 w-6 text-white animate-pulse" />
          </div>
          <p className="text-sm text-muted-foreground animate-pulse">Checking session…</p>
        </div>
      </div>
    );
  }

  if (user) return null;

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      if (name.trim()) {
        await updateProfile(cred.user, { displayName: name.trim() });
      }
      router.push("/dashboard");
    } catch (err) {
      setError(getFriendlyError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleGoogle = async () => {
    setError("");
    setGoogleLoading(true);
    try {
      // Try popup first
      await signInWithPopup(auth, googleProvider);
      router.push("/dashboard");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "";
      if (msg.includes("auth/popup-blocked") || msg.includes("auth/popup-closed-by-user")) {
        // Fallback to full-page redirect
        try {
          await signInWithRedirect(auth, googleProvider);
          // Page reloads; result is handled in the useEffect above
        } catch (redirectErr) {
          setError(getFriendlyError(redirectErr));
          setGoogleLoading(false);
        }
      } else {
        const friendly = getFriendlyError(err);
        if (friendly) setError(friendly);
        setGoogleLoading(false);
      }
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-xl shadow-emerald-500/25 mb-4">
            <TrendingUp className="h-7 w-7 text-white" />
          </div>
          <h1 className="font-display text-2xl font-bold">Create your account</h1>
          <p className="text-muted-foreground text-sm mt-1">Start your financial journey with Finova</p>
        </div>

        <Card className="border-border/60 bg-card/80 backdrop-blur shadow-xl">
          <CardContent className="pt-6 space-y-4">
            <Button
              type="button"
              variant="outline"
              className="w-full gap-2"
              onClick={handleGoogle}
              disabled={googleLoading || loading}
            >
              {googleLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <GoogleIcon />}
              {googleLoading ? "Redirecting to Google…" : "Continue with Google"}
            </Button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-border/60" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Or continue with email</span>
              </div>
            </div>

            <form onSubmit={handleRegister} className="space-y-4">
              {error && (
                <div className="flex items-start gap-2 rounded-xl bg-destructive/10 border border-destructive/20 px-3 py-2.5 text-sm text-destructive">
                  <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="name">Full Name <span className="text-muted-foreground">(optional)</span></Label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="name"
                    placeholder="John Doe"
                    className="pl-10"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    autoComplete="name"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    className="pl-10"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoComplete="email"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Min. 6 characters"
                    className="pl-10 pr-10"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    required
                    minLength={6}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    tabIndex={-1}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {password.length > 0 && password.length < 6 && (
                  <p className="text-xs text-destructive">Password must be at least 6 characters</p>
                )}
              </div>

              <Button type="submit" variant="gradient" className="w-full" disabled={loading || googleLoading}>
                {loading ? (
                  <><Loader2 className="h-4 w-4 animate-spin" /> Creating account…</>
                ) : "Create Account"}
              </Button>
            </form>
          </CardContent>
        </Card>

        <p className="text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/login" className="text-emerald-600 dark:text-emerald-400 font-medium hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
