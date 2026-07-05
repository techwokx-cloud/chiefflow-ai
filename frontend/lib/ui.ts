import { Mail, DollarSign, Scale, Search, Calendar, Headset, FileText, MessageSquare, Globe } from "lucide-react";

export const STATUS_STYLE: Record<string, string> = {
  received: "bg-slate-500/15 text-slate-300 border-slate-500/30",
  processing: "bg-primary/15 text-primary border-primary/30 animate-pulseSoft",
  needs_approval: "bg-accent/15 text-accent border-accent/30",
  approved: "bg-secondary/15 text-secondary border-secondary/30",
  executed: "bg-secondary/15 text-secondary border-secondary/30",
  rejected: "bg-red-500/15 text-red-400 border-red-500/30",
  archived: "bg-slate-600/15 text-muted border-slate-600/30",
};

export const STATUS_LABEL: Record<string, string> = {
  received: "Received",
  processing: "Processing",
  needs_approval: "Needs Approval",
  approved: "Approved",
  executed: "Completed",
  rejected: "Rejected",
  archived: "Archived",
};

export const PRIORITY_STYLE: Record<string, string> = {
  low: "text-muted",
  normal: "text-primary",
  high: "text-accent",
  urgent: "text-red-400",
};

export const AGENT_COLOR: Record<string, string> = {
  email: "#60A5FA",
  finance: "#16A34A",
  legal: "#A78BFA",
  research: "#22D3EE",
  calendar: "#EA580C",
  support: "#F472B6",
  manager: "#F8FAFC",
};

export const AGENT_ICON: Record<string, any> = {
  email: Mail, finance: DollarSign, legal: Scale, research: Search, calendar: Calendar, support: Headset,
};

export const SOURCE_ICON: Record<string, any> = {
  email: Mail, pdf: FileText, docx: FileText, notes: FileText, chat: MessageSquare, api: Globe,
};

export function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso + "Z").getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}
