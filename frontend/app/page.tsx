"use client";
import Link from "next/link";
import { Hexagon, Mail, DollarSign, Scale, Search, Calendar, Headset, ArrowRight, PlayCircle } from "lucide-react";

const AGENTS = [
  { icon: Mail, label: "Email Agent", pos: "top-0 left-4" },
  { icon: DollarSign, label: "Finance Agent", pos: "top-0 right-4" },
  { icon: Scale, label: "Legal Agent", pos: "top-20 -right-2" },
  { icon: Search, label: "Research Agent", pos: "bottom-8 right-2" },
  { icon: Calendar, label: "Calendar Agent", pos: "bottom-0 left-1/2 -translate-x-1/2" },
  { icon: Headset, label: "Support Agent", pos: "top-20 -left-2" },
];

export default function Landing() {
  return (
    <main className="min-h-screen bg-bg relative overflow-hidden">
      <div className="absolute -top-40 right-0 w-[500px] h-[500px] rounded-full bg-primary/10 blur-3xl" />
      <div className="absolute bottom-0 -left-40 w-[400px] h-[400px] rounded-full bg-secondary/10 blur-3xl" />

      <nav className="relative z-10 flex items-center justify-between px-8 py-5 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary/15 border border-primary/40 flex items-center justify-center">
            <Hexagon size={16} className="text-primary" />
          </div>
          <span className="font-bold">ChiefFlow AI</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-muted">
          <span>Features</span><span>Solutions</span><span>Pricing</span><span>Docs</span>
        </div>
        <Link href="/dashboard" className="bg-primary hover:bg-primaryHover text-sm font-medium px-4 py-2 rounded-lg transition-colors">
          Get Started
        </Link>
      </nav>

      <section className="relative z-10 max-w-6xl mx-auto px-8 pt-20 pb-16 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <div className="inline-flex items-center gap-2 text-xs text-secondary font-semibold mb-6 tracking-wide">
            BUILT FOR AMD DEVELOPER HACKATHON 2026
          </div>
          <h1 className="text-5xl font-extrabold leading-tight mb-4">
            ChiefFlow <span className="text-primary">AI</span>
          </h1>
          <p className="text-xl text-muted mb-6">The AI Chief of Staff for Modern Businesses</p>
          <p className="text-sm text-slate-300 leading-relaxed mb-8 max-w-md">
            Transform emails, documents, meetings, and business operations into autonomous workflows powered by AI Agents — with humans approving every high-impact step.
          </p>
          <div className="flex items-center gap-3">
            <Link href="/dashboard" className="flex items-center gap-2 bg-primary hover:bg-primaryHover font-semibold px-5 py-3 rounded-lg text-sm transition-colors shadow-glow">
              Enter Live Demo <ArrowRight size={16} />
            </Link>
            <button className="flex items-center gap-2 border border-border px-5 py-3 rounded-lg text-sm text-muted hover:text-text transition-colors">
              <PlayCircle size={16} /> Watch Demo
            </button>
          </div>

          <div className="grid grid-cols-4 gap-4 mt-12 max-w-md">
            {[["98%", "Task Automation"], ["72%", "Cost Reduction"], ["5x", "Productivity"], ["24/7", "AI Workforce"]].map(([n, l], i) => (
              <div key={l}>
                <div className={`text-xl font-extrabold ${["text-primary", "text-secondary", "text-accent", "text-text"][i]}`}>{n}</div>
                <div className="text-[10px] text-muted mt-0.5 leading-tight">{l}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative h-[420px] hidden md:block">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-40 h-40 rounded-2xl rotate-45 bg-gradient-to-br from-primary/30 to-primary/5 border border-primary/50 flex items-center justify-center shadow-glow">
              <div className="-rotate-45 text-center">
                <Hexagon className="mx-auto text-primary mb-1" size={22} />
                <div className="text-[10px] font-bold">ChiefFlow AI</div>
              </div>
            </div>
          </div>
          {AGENTS.map(({ icon: Icon, label, pos }) => (
            <div key={label} className={`absolute ${pos} flex flex-col items-center gap-1.5`}>
              <div className="w-14 h-14 rounded-2xl bg-card border border-border flex items-center justify-center text-primary">
                <Icon size={20} />
              </div>
              <span className="text-[10px] text-muted whitespace-nowrap">{label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="relative z-10 max-w-6xl mx-auto px-8 pb-20">
        <div className="text-center text-xs text-muted mb-4 tracking-wide">POWERED BY</div>
        <div className="flex items-center justify-center gap-10 text-sm text-slate-300 flex-wrap">
          <span>AMD Developer Cloud</span><span>Fireworks AI</span><span>Gemma</span><span>ROCm</span>
        </div>
        <div className="text-center text-[10px] text-muted/60 mt-6">Built with Claude AI</div>
      </section>
    </main>
  );
}
