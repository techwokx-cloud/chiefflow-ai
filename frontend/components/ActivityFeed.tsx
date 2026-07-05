import { ActivityEntry } from "@/lib/types";
import { AGENT_COLOR, timeAgo } from "@/lib/ui";
import { Bot, User } from "lucide-react";

export default function ActivityFeed({ items }: { items: ActivityEntry[] }) {
  if (items.length === 0) {
    return <div className="text-sm text-muted py-8 text-center">No activity yet.</div>;
  }
  return (
    <div className="space-y-0">
      {items.map((a, i) => {
        const isAgent = !a.actor.startsWith("user:");
        const color = isAgent ? (AGENT_COLOR[a.actor] || "#94A3B8") : "#F8FAFC";
        const label = isAgent ? `${a.actor.charAt(0).toUpperCase()}${a.actor.slice(1)} Agent` : a.actor.replace("user:", "");
        return (
          <div key={a.id} className="flex gap-3 pb-4 relative">
            {i < items.length - 1 && <div className="absolute left-[15px] top-8 bottom-0 w-px bg-border" />}
            <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 z-10" style={{ backgroundColor: `${color}22`, color }}>
              {isAgent ? <Bot size={14} /> : <User size={14} />}
            </div>
            <div className="flex-1 min-w-0 pt-0.5">
              <div className="text-xs">
                <span className="font-semibold">{label}</span>
                <span className="text-muted"> · {a.action.replace(/_/g, " ")}</span>
              </div>
              <div className="text-xs text-muted mt-0.5 line-clamp-2">{a.detail}</div>
              <div className="text-[10px] text-muted mt-1 flex items-center gap-2">
                <span>{timeAgo(a.created_at)}</span>
                {a.model_used && <span className="px-1.5 py-0.5 rounded bg-card border border-border">{a.model_used}</span>}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
