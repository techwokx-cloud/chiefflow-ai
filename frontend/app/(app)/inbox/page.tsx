"use client";
import { useEffect, useState, useCallback } from "react";
import Topbar from "@/components/Topbar";
import WorkflowCard from "@/components/WorkflowCard";
import { api } from "@/lib/api";
import { WorkflowItem } from "@/lib/types";
import { Plus, X } from "lucide-react";

const FILTERS = ["all", "received", "processing", "needs_approval", "executed", "rejected", "archived"];

export default function InboxPage() {
  const [items, setItems] = useState<WorkflowItem[]>([]);
  const [filter, setFilter] = useState("all");
  const [showCompose, setShowCompose] = useState(false);
  const [form, setForm] = useState({ source: "email", title: "", sender: "", raw_text: "" });
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setItems(await api.listInbox(filter === "all" ? undefined : filter));
  }, [filter]);

  useEffect(() => { load(); }, [load]);

  const submit = async () => {
    if (!form.title || !form.raw_text) return;
    setSubmitting(true);
    try {
      await api.createInboxItem(form);
      setShowCompose(false);
      setForm({ source: "email", title: "", sender: "", raw_text: "" });
      load();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Topbar title="Unified Inbox" subtitle="Every email, document, and request flowing through your business, in one place." />
      <div className="p-8">
        <div className="flex items-center justify-between mb-5">
          <div className="flex gap-2 flex-wrap">
            {FILTERS.map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`text-xs px-3 py-1.5 rounded-full border capitalize transition-colors ${
                  filter === f ? "bg-primary/15 border-primary/40 text-primary" : "border-border text-muted hover:text-text"
                }`}
              >
                {f.replace("_", " ")}
              </button>
            ))}
          </div>
          <button
            onClick={() => setShowCompose(true)}
            className="flex items-center gap-1.5 bg-primary hover:bg-primaryHover text-xs font-medium px-3 py-2 rounded-lg transition-colors"
          >
            <Plus size={14} /> New Item
          </button>
        </div>

        {showCompose && (
          <div className="glass rounded-card p-5 mb-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-semibold">Paste an email, note, or request</span>
              <button onClick={() => setShowCompose(false)} className="text-muted hover:text-text"><X size={16} /></button>
            </div>
            <div className="grid md:grid-cols-2 gap-3 mb-3">
              <select
                value={form.source}
                onChange={(e) => setForm({ ...form, source: e.target.value })}
                className="bg-surface border border-border rounded-lg px-3 py-2 text-sm outline-none"
              >
                {["email", "notes", "chat", "api"].map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
              <input
                placeholder="Sender (optional)"
                value={form.sender}
                onChange={(e) => setForm({ ...form, sender: e.target.value })}
                className="bg-surface border border-border rounded-lg px-3 py-2 text-sm outline-none"
              />
            </div>
            <input
              placeholder="Subject / Title"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              className="w-full bg-surface border border-border rounded-lg px-3 py-2 text-sm outline-none mb-3"
            />
            <textarea
              placeholder="Paste the message content here..."
              value={form.raw_text}
              onChange={(e) => setForm({ ...form, raw_text: e.target.value })}
              rows={5}
              className="w-full bg-surface border border-border rounded-lg px-3 py-2 text-sm outline-none mb-3 resize-none"
            />
            <button
              onClick={submit}
              disabled={submitting}
              className="bg-primary hover:bg-primaryHover text-sm font-medium px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
            >
              {submitting ? "Processing with AI..." : "Submit to ChiefFlow AI"}
            </button>
          </div>
        )}

        <div className="grid md:grid-cols-3 gap-4">
          {items.length === 0 && <div className="text-sm text-muted col-span-3 text-center py-12">No items in this view.</div>}
          {items.map((item) => <WorkflowCard key={item.id} item={item} />)}
        </div>
      </div>
    </>
  );
}
