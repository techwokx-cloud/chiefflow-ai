"use client";
import { useEffect, useState } from "react";
import Topbar from "@/components/Topbar";
import AgentCard from "@/components/AgentCard";
import { api } from "@/lib/api";
import { Agent } from "@/lib/types";

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);

  useEffect(() => { api.listAgents().then(setAgents); }, []);

  return (
    <>
      <Topbar title="AI Agents" subtitle="Manage your AI workforce. The Manager Agent routes work to these six specialists." />
      <div className="p-8">
        <div className="grid md:grid-cols-3 gap-4">
          {agents.map((a) => <AgentCard key={a.id} agent={a} />)}
        </div>
      </div>
    </>
  );
}
