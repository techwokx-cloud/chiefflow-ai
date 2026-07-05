"use client";
import { useEffect, useState, useCallback } from "react";
import Topbar from "@/components/Topbar";
import StatCard from "@/components/StatCard";
import UploadDropzone from "@/components/UploadDropzone";
import WorkflowCard from "@/components/WorkflowCard";
import ActivityFeed from "@/components/ActivityFeed";
import { api } from "@/lib/api";
import { WorkflowItem, Analytics, ActivityEntry } from "@/lib/types";
import { Inbox, CheckCircle2, Clock3, TrendingUp } from "lucide-react";

const COLUMNS: { key: string; label: string; statuses: string[] }[] = [
  { key: "new", label: "New / Processing", statuses: ["received", "processing"] },
  { key: "review", label: "Needs Approval", statuses: ["needs_approval"] },
  { key: "done", label: "Completed", statuses: ["executed", "approved"] },
];

export default function Dashboard() {
  const [items, setItems] = useState<WorkflowItem[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [activity, setActivity] = useState<ActivityEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    const [i, a, act] = await Promise.all([api.listInbox(), api.getAnalytics(), api.listActivity(8)]);
    setItems(i);
    setAnalytics(a);
    setActivity(act);
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <>
      <Topbar title="Good morning, George 👋" subtitle="Here's what's happening across your business today." />
      <div className="p-8 space-y-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard icon={Inbox} label="Total Workflows" value={items.length} color="text-primary" />
          <StatCard icon={Clock3} label="Pending Review" value={items.filter((i) => i.status === "needs_approval").length} color="text-accent" />
          <StatCard icon={CheckCircle2} label="Completed" value={analytics?.tasks_automated ?? 0} color="text-secondary" />
          <StatCard icon={TrendingUp} label="Hours Saved" value={analytics?.hours_saved ?? 0} suffix="hrs" color="text-text" />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div>
              <h2 className="text-sm font-semibold mb-3 text-muted uppercase tracking-wide">Upload a Document</h2>
              <UploadDropzone onDone={load} />
            </div>

            <div>
              <h2 className="text-sm font-semibold mb-3 text-muted uppercase tracking-wide">Workflow Board</h2>
              {loading ? (
                <div className="text-sm text-muted">Loading workflows...</div>
              ) : (
                <div className="grid md:grid-cols-3 gap-4">
                  {COLUMNS.map((col) => {
                    const colItems = items.filter((i) => col.statuses.includes(i.status));
                    return (
                      <div key={col.key} className="space-y-3">
                        <div className="flex items-center justify-between px-1">
                          <span className="text-xs font-semibold text-muted">{col.label}</span>
                          <span className="text-xs text-muted bg-card px-1.5 rounded">{colItems.length}</span>
                        </div>
                        <div className="space-y-3 max-h-[560px] overflow-y-auto pr-1">
                          {colItems.length === 0 && <div className="text-xs text-muted py-4 text-center border border-dashed border-border rounded-card">Empty</div>}
                          {colItems.map((item) => <WorkflowCard key={item.id} item={item} />)}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          <div className="glass rounded-card p-5 h-fit">
            <h2 className="text-sm font-semibold mb-4 text-muted uppercase tracking-wide">Activity Timeline</h2>
            <ActivityFeed items={activity} />
          </div>
        </div>
      </div>
    </>
  );
}
