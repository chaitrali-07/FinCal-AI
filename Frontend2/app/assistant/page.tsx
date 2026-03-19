"use client";

import { useState, useRef, useEffect } from "react";
import { chatWithAssistant } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Bot,
  Send,
  User,
  Loader2,
  Sparkles,
  TrendingUp,
  AlertCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  error?: boolean;
};

const SUGGESTIONS = [
  "How does SIP investing work?",
  "What's the difference between FD and RD?",
  "How is EMI calculated?",
  "Explain income tax slabs",
];

function AssistantContent() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await chatWithAssistant(text.trim());
      const reply =
        typeof res === "string"
          ? res
          : res?.response ?? res?.message ?? res?.reply ?? JSON.stringify(res);

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: reply,
        },
      ]);
    } catch (err: unknown) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "Sorry, I couldn't get a response. Please try again.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  const initials = user?.displayName
    ? user.displayName.split(" ").map((n) => n[0]).join("").toUpperCase()
    : user?.email?.[0]?.toUpperCase() ?? "U";

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* Header */}
      <div className="border-b border-border/40 bg-background/80 backdrop-blur px-4 sm:px-6 py-4">
        <div className="container max-w-4xl mx-auto flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-lg">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-display font-bold text-lg leading-none">AI Financial Assistant</h1>
            <p className="text-xs text-muted-foreground mt-0.5">Powered by Finova AI</p>
          </div>
          <div className="ml-auto flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs text-muted-foreground">Online</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto chat-scroll px-4 sm:px-6 py-6">
        <div className="container max-w-4xl mx-auto space-y-6">
          {/* Welcome */}
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-xl mb-5">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <h2 className="font-display text-2xl font-bold mb-2">
                How can I help you today?
              </h2>
              <p className="text-muted-foreground max-w-sm mb-8">
                Ask me anything about investments, loans, taxes, or financial planning.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => sendMessage(s)}
                    className="rounded-xl border border-border/60 bg-card/60 p-3 text-sm text-left hover:border-emerald-500/40 hover:bg-accent transition-all duration-200"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Message bubbles */}
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={cn(
                "flex gap-3",
                msg.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              {/* Avatar */}
              {msg.role === "assistant" ? (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 shadow-md mt-1">
                  <TrendingUp className="h-4 w-4 text-white" />
                </div>
              ) : (
                <Avatar className="h-8 w-8 shrink-0 mt-1">
                  <AvatarImage src={user?.photoURL ?? ""} />
                  <AvatarFallback className="bg-gradient-to-br from-slate-600 to-slate-700 text-white text-xs font-bold">
                    {initials}
                  </AvatarFallback>
                </Avatar>
              )}

              {/* Bubble */}
              <div
                className={cn(
                  "max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
                  msg.role === "user"
                    ? "bg-gradient-to-br from-emerald-500 to-teal-500 text-white rounded-tr-sm"
                    : msg.error
                    ? "bg-destructive/10 border border-destructive/20 text-destructive rounded-tl-sm"
                    : "bg-card border border-border/60 rounded-tl-sm"
                )}
              >
                {msg.error && (
                  <AlertCircle className="h-3.5 w-3.5 inline mr-1 mb-0.5" />
                )}
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))}

          {/* Loading */}
          {loading && (
            <div className="flex gap-3">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 shadow-md mt-1">
                <TrendingUp className="h-4 w-4 text-white" />
              </div>
              <div className="rounded-2xl rounded-tl-sm bg-card border border-border/60 px-4 py-3">
                <div className="flex gap-1.5 items-center h-5">
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:0ms]" />
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:150ms]" />
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-border/40 bg-background/80 backdrop-blur px-4 sm:px-6 py-4">
        <div className="container max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about investments, loans, taxes..."
              className="flex-1 bg-card/60 border-border/60"
              disabled={loading}
            />
            <Button
              type="submit"
              variant="gradient"
              size="icon"
              disabled={!input.trim() || loading}
              className="shrink-0"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>
          <p className="text-xs text-muted-foreground text-center mt-2">
            AI responses are for educational purposes only, not financial advice.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function AssistantPage() {
  return (
    <ProtectedRoute>
      <AssistantContent />
    </ProtectedRoute>
  );
}
