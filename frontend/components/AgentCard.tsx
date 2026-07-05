import { Agent } from "@/lib/types";
import { AGENT_COLOR, AGENT_ICON } from "@/lib/ui";

export default function AgentCard({ agent }: { agent: Agent }) {
  const Icon = AGENT_ICON[agent.key];
  const color = AGENT_COLOR[agent.key];
  const statusStyle =
    agent.status === "running" ? "bg-secondary/15 text-secondary border-secondary/30" :
    agent.status === "completed" ? "bg-primary/15 text-primary border-primary/30" :
    "bg-slate-500/15 text-muted border-slate-500/30";

  return (
    <div className="glass rounded-card p-4 card-hover">
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${color}22`, color }}>
          {Icon && <Icon size={18} />}
        </div>
        <span className={`text-[10px] px-2 py-0.5 rounded-full border capitalize ${statusStyle}`}>{agent.status}</span>
      </div>
      <div className="font-semibold text-sm">{agent.name}</div>
      <div className="text-xs text-muted mt-0.5 mb-3">{agent.description}</div>
      <div className="flex items-center justify-between text-[11px] text-muted border-t border-border pt-2.5">
        <span>{(agent.accuracy * 100).toFixed(0)}% accuracy</span>
        <span>{agent.tasks_handled} handled</span>
      </div>
      {agent.current_task && (
        <div className="text-[10px] text-primary mt-2 truncate">→ {agent.current_task}</div>
      )}
    </div>
  );
}
