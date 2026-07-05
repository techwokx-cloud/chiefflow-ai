"use client";
import { useEffect, useState, useCallback, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Topbar from "@/components/Topbar";
import { api } from "@/lib/api";
import { WorkflowItem } from "@/lib/types";
import { STATUS_STYLE, STATUS_LABEL, AGENT_COLOR, AGENT_ICON, timeAgo } from "@/lib/ui";
import { CheckCircle2, XCircle, RefreshCcw, ArrowLeft, Sparkles } from "lucide-react";

function Field({ label, value }: { label: string; value: any }) {
  if (value === undefined || value === null || value === "" || (Array.isArray(value) && value.length === 0)) return null;
  return (
    <div className="border-b border-border py-2.5 flex items-start justify-between gap-4">
      <span className="text-xs text-muted capitalize shrink-0">{label.replace(/_/g, " ")}</span>
      <span className="text-sm text-right break-words">{Array.isArray(value) ? value.join(", ") : String(value)}</span>
    </div>
  );
}

function WorkflowDetailInner() {
  const searchParams = useSearchParams();
  const id = searchParams.get("id") || "";
  const router = useRouter();
  const [item, setItem] = useState<WorkflowItem | null>(null);
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => { if (id) setItem(await api.getInboxItem(id)); }, [id]);
  useEffect(() => { load(); }, [load]);

  const decide = async (approve: boolean) => {
    setBusy(true);
    try {
      const updated = await api.approve(id, approve);
      setItem(updated);
    } finally {
      setBusy(false);
    }
  };

  if (!item) return <div className="p-8 text-sm text-muted">Loading...</div>;

  const Icon = item.assigned_agent_key ? AGENT_ICON[item.assigned_agent_key] : Sparkles;
  const color = item.assigned_agent_key ? AGENT_COLOR[item.assigned_agent_key] : "#94A3B8";
  const { ai_draft, ...otherFields } = item.extracted_data || {};

  return (
    <>
      <Topbar title="Workflow Review" />
      <div className="p-8 max-w-4xl">
        <button onClick={() => router.back()} className="flex items-center gap-1.5 text-xs text-muted hover:text-text mb-5">
          <ArrowLeft size={14} /> Back
        </button>

        <div className="glass rounded-card p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${color}22`, color }}>
                <Icon size={20} />
              </div>
              <div>
                <div className="font-bold">{item.title}</div>
                <div className="text-xs text-muted mt-0.5">
                  {item.sender && <>{item.sender} · </>}via {item.source} · {timeAgo(item.created_at)}
                </div>
              </div>
            </div>
            <span className={`text-xs px-3 py-1 rounded-full border capitalize ${STATUS_STYLE[item.status]}`}>
              {STATUS_LABEL[item.status] || item.status}
            </span>
          </div>

          <div className="grid grid-cols-3 gap-3 mb-5">
            <div className="bg-surface rounded-lg p-3">
              <div className="text-[10px] text-muted uppercase mb-1">Detected Intent</div>
              <div className="text-sm font-semibold capitalize">{item.intent?.replace("_", " ") || "—"}</div>
            </div>
            <div className="bg-surface rounded-lg p-3">
              <div className="text-[10px] text-muted uppercase mb-1">Assigned Agent</div>
              <div className="text-sm font-semibold capitalize">{item.assigned_agent_key || "—"} Agent</div>
            </div>
            <div className="bg-surface rounded-lg p-3">
              <div className="text-[10px] text-muted uppercase mb-1">Model Used</div>
              <div className="text-sm font-semibold">{item.model_used || "—"}</div>
            </div>
          </div>

          {item.ai_summary && (
            <div className="mb-5">
              <div className="text-xs font-semibold text-muted uppercase mb-2">Summary</div>
              <p className="text-sm text-slate-200 leading-relaxed">{item.ai_summary}</p>
            </div>
          )}

          {Object.keys(otherFields).length > 0 && (
            <div className="mb-5">
              <div className="text-xs font-semibold text-muted uppercase mb-1">Extracted Details</div>
              {Object.entries(otherFields).map(([k, v]) => <Field key={k} label={k} value={v} />)}
            </div>
          )}

          {item.suggested_action && (
            <div className="mb-5 bg-primary/10 border border-primary/30 rounded-lg p-4">
              <div className="text-xs font-semibold text-primary uppercase mb-1">Suggested Action</div>
              <p className="text-sm">{item.suggested_action}</p>
            </div>
          )}

          {ai_draft && (
            <div className="mb-5">
              <div className="text-xs font-semibold text-muted uppercase mb-2">AI Draft</div>
              <div className="bg-surface border border-border rounded-lg p-4 text-sm whitespace-pre-wrap text-slate-200">{String(ai_draft)}</div>
            </div>
          )}

          {item.status === "needs_approval" && (
            <div className="flex gap-3 pt-2">
              <button
                onClick={() => decide(true)}
                disabled={busy}
                className="flex items-center gap-2 bg-secondary hover:bg-secondary/80 font-semibold px-5 py-2.5 rounded-lg text-sm transition-colors disabled:opacity-50"
              >
                <CheckCircle2 size={16} /> Approve
              </button>
              <button
                onClick={() => decide(false)}
                disabled={busy}
                className="flex items-center gap-2 border border-border hover:border-red-500/50 hover:text-red-400 font-semibold px-5 py-2.5 rounded-lg text-sm transition-colors disabled:opacity-50"
              >
                <XCircle size={16} /> Reject
              </button>
            </div>
          )}

          {item.status === "executed" && (
            <div className="flex items-center gap-2 text-secondary text-sm font-semibold pt-2">
              <CheckCircle2 size={16} /> Approved & Executed
            </div>
          )}
          {item.status === "rejected" && (
            <div className="flex items-center gap-2 text-red-400 text-sm font-semibold pt-2">
              <XCircle size={16} /> Rejected
            </div>
          )}
        </div>

        <button
          onClick={async () => { setBusy(true); setItem(await api.reprocess(id)); setBusy(false); }}
          disabled={busy}
          className="flex items-center gap-1.5 text-xs text-muted hover:text-text disabled:opacity-50"
        >
          <RefreshCcw size={13} /> Reprocess with AI
        </button>
      </div>
    </>
  );
}

export default function WorkflowDetail() {
  return (
    <Suspense fallback={<div className="p-8 text-sm text-muted">Loading...</div>}>
      <WorkflowDetailInner />
    </Suspense>
  );
}
