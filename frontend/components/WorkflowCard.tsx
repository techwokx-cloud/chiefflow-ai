"use client";
import Link from "next/link";
import { STATUS_STYLE, STATUS_LABEL, PRIORITY_STYLE, SOURCE_ICON, AGENT_COLOR, timeAgo } from "@/lib/ui";
import { WorkflowItem } from "@/lib/types";

export default function WorkflowCard({ item }: { item: WorkflowItem }) {
  const SourceIcon = SOURCE_ICON[item.source] || SOURCE_ICON.chat;
  const agentColor = item.assigned_agent_key ? AGENT_COLOR[item.assigned_agent_key] : "#94A3B8";

  return (
    <Link
      href={`/workflow?id=${item.id}`}
      className="block glass rounded-card p-4 card-hover animate-fadeInUp"
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-7 h-7 rounded-md bg-card flex items-center justify-center shrink-0" style={{ color: agentColor }}>
            <SourceIcon size={14} />
          </div>
          <span className="text-xs text-muted capitalize truncate">{item.source}</span>
        </div>
        <span className={`text-[10px] px-2 py-0.5 rounded-full border shrink-0 ${STATUS_STYLE[item.status] || ""}`}>
          {STATUS_LABEL[item.status] || item.status}
        </span>
      </div>

      <div className="font-semibold text-sm leading-snug mb-1.5 line-clamp-2">{item.title}</div>

      {item.ai_summary && (
        <p className="text-xs text-muted line-clamp-2 mb-2">{item.ai_summary}</p>
      )}

      <div className="flex items-center justify-between mt-3 text-[11px]">
        <div className="flex items-center gap-2">
          {item.intent && (
            <span className="px-2 py-0.5 rounded-full bg-card border border-border capitalize text-muted">{item.intent.replace("_", " ")}</span>
          )}
          {item.priority !== "normal" && (
            <span className={`font-medium capitalize ${PRIORITY_STYLE[item.priority]}`}>{item.priority}</span>
          )}
        </div>
        <span className="text-muted">{timeAgo(item.created_at)}</span>
      </div>
    </Link>
  );
}
