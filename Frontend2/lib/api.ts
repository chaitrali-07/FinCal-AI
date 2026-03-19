const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function getHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  return res.json();
}

export async function getCalculators() {
  const res = await fetch(`${BASE_URL}/api/calculators`);
  if (!res.ok) throw new Error("Failed to fetch calculators");
  return res.json();
}

export async function calculate(type: string, body: Record<string, number>, token?: string | null) {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}/api/calculators/${type}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail || err?.error || `Calculation failed (${res.status})`);
  }
  return res.json();
}

export async function chatWithAssistant(message: string) {
  const res = await fetch(`${BASE_URL}/api/assistant/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail || err?.error || "Failed to get response");
  }
  const data = await res.json();
  return {
    response: data.reply ?? data.response ?? data.message ?? data.answer ?? JSON.stringify(data),
  };
}

export async function getHistory(token: string) {
  const res = await fetch(`${BASE_URL}/api/history`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch history");
  return res.json();
}

export async function deleteHistoryRecord(id: string, token: string) {
  const res = await fetch(`${BASE_URL}/api/history/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to delete record");
  return res.json();
}