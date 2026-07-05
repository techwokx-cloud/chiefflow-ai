"use client";
import { useEffect, useState } from "react";
import Topbar from "@/components/Topbar";
import StatCard from "@/components/StatCard";
import { api } from "@/lib/api";
import { Analytics } from "@/lib/types";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { Mail, FileText, CheckCircle2, Clock3, DollarSign, Target, Users, Percent } from "lucide-react";

const TIER_COLORS: Record<string, string> = { simple: "#16A34A", moderate: "#2563EB", complex: "#EA580C" };
const TIER_LABEL: Record<string, string> = { simple: "Gemma (Simple)", moderate: "AMD GPU (Moderate)", complex: "Fireworks AI (Complex)" };

export default function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);

  useEffect(() => { api.getAnalytics().then(setData); }, []);

  const chartData = data
    ? Object.entries(data.model_tier_breakdown)
        .filter(([, v]) => v > 0)
        .map(([k, v]) => ({ name: TIER_LABEL[k], value: v, color: TIER_COLORS[k] }))
    : [];

  return (
    <>
      <Topbar title="Analytics" subtitle="Business impact and AI routing efficiency, computed live from your workflow data." />
      <div className="p-8 space-y-8">
        {data && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard icon={Mail} label="Emails Processed" value={data.emails_processed} color="text-primary" />
            <StatCard icon={FileText} label="Documents Reviewed" value={data.documents_reviewed} color="text-secondary" />
            <StatCard icon={CheckCircle2} label="Tasks Automated" value={data.tasks_automated} color="text-accent" />
            <StatCard icon={Clock3} label="Hours Saved" value={data.hours_saved} suffix="hrs" color="text-text" />
            <StatCard icon={DollarSign} label="Cost Saved" value={`$${data.cost_saved_usd}`} color="text-secondary" />
            <StatCard icon={Target} label="AI Accuracy" value={`${data.ai_accuracy}%`} color="text-primary" />
            <StatCard icon={Percent} label="Approval Rate" value={`${data.approval_rate}%`} color="text-accent" />
            <StatCard icon={Users} label="Active Agents" value={data.active_agents} color="text-text" />
          </div>
        )}

        <div className="glass rounded-card p-6">
          <h2 className="text-sm font-semibold mb-1 text-muted uppercase tracking-wide">AI Model Routing</h2>
          <p className="text-xs text-muted mb-4">Every task uses the cheapest model capable of producing acceptable quality.</p>
          {chartData.length === 0 ? (
            <div className="text-sm text-muted py-8 text-center">No routed tasks yet — process a workflow to see the breakdown.</div>
          ) : (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData} dataKey="value" nameKey="name" innerRadius={60} outerRadius={100} paddingAngle={3}>
                    {chartData.map((entry, i) => <Cell key={i} fill={entry.color} stroke="none" />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: "#101826", border: "1px solid #1E293B", borderRadius: 8, fontSize: 12 }} />
                  <Legend wrapperStyle={{ fontSize: 12 }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
