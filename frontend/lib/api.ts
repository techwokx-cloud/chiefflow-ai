import { WorkflowItem, Agent, ActivityEntry, Analytics } from "./types";

const TOKEN_KEY = "chiefflow_demo_token";
// In production (static export served by FastAPI) this stays empty and calls
// are same-origin. For `next dev` without Docker, set NEXT_PUBLIC_API_BASE=http://localhost:8000
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";
let inflightAuth: Promise<string> | null = null;

async function getToken(forceRefresh = false): Promise<string> {
  if (typeof window === "undefined") return "";
  if (forceRefresh) {
    window.localStorage.removeItem(TOKEN_KEY);
    inflightAuth = null;
  } else {
    const cached = window.localStorage.getItem(TOKEN_KEY);
    if (cached) return cached;
  }

  if (!inflightAuth) {
    inflightAuth = fetch(`${API_BASE}/api/auth/demo-login`, { method: "POST" })
      .then((r) => r.json())
      .then((data) => {
        window.localStorage.setItem(TOKEN_KEY, data.access_token);
        inflightAuth = null;
        return data.access_token as string;
      });
  }
  return inflightAuth;
}

async function request<T>(path: string, options: RequestInit = {}, _retried = false): Promise<T> {
  const token = await getToken();
  const res = await fetch(`${API_BASE}/api${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.body && !(options.body instanceof FormData) ? { "Content-Type": "application/json" } : {}),
      ...(options.headers || {}),
    },
  });

  if (res.status === 401 && !_retried) {
    // Cached token is stale/invalid (e.g. server JWT_SECRET rotated on redeploy).
    // Force a fresh login once and retry the same request before giving up.
    await getToken(true);
    return request<T>(path, options, true);
  }

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

export const api = {
  listInbox: (status?: string) => request<WorkflowItem[]>(`/inbox${status ? `?status=${status}` : ""}`),
  getInboxItem: (id: string) => request<WorkflowItem>(`/inbox/${id}`),
  createInboxItem: (payload: { source: string; title: string; sender?: string; raw_text: string }) =>
    request<WorkflowItem>(`/inbox`, { method: "POST", body: JSON.stringify(payload) }),
  reprocess: (id: string) => request<WorkflowItem>(`/inbox/${id}/reprocess`, { method: "POST" }),
  approve: (id: string, approve: boolean, note?: string) =>
    request<WorkflowItem>(`/inbox/${id}/approve`, { method: "POST", body: JSON.stringify({ approve, note }) }),
  archive: (id: string) => request<WorkflowItem>(`/inbox/${id}/archive`, { method: "POST" }),
  uploadDocument: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<WorkflowItem>(`/documents/upload`, { method: "POST", body: form });
  },
  listAgents: () => request<Agent[]>(`/agents`),
  listActivity: (limit = 50) => request<ActivityEntry[]>(`/activity?limit=${limit}`),
  getAnalytics: () => request<Analytics>(`/analytics`),
};
