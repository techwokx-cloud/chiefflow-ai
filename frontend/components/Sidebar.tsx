"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Inbox, FileText, Bot, BarChart3, Settings, Hexagon,
} from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/inbox", label: "Inbox", icon: Inbox },
  { href: "/documents", label: "Documents", icon: FileText },
  { href: "/agents", label: "AI Agents", icon: Bot },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="w-60 shrink-0 h-screen sticky top-0 border-r border-border bg-surface/60 flex flex-col">
      <Link href="/" className="flex items-center gap-2 px-5 py-5">
        <div className="w-9 h-9 rounded-lg bg-primary/15 border border-primary/40 flex items-center justify-center">
          <Hexagon size={18} className="text-primary" strokeWidth={2.5} />
        </div>
        <div>
          <div className="font-bold text-sm leading-none">ChiefFlow AI</div>
          <div className="text-[10px] text-muted mt-1">AI Chief of Staff</div>
        </div>
      </Link>

      <nav className="flex-1 px-3 py-2 space-y-1">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                active ? "bg-primary/15 text-primary border border-primary/30" : "text-muted hover:text-text hover:bg-card"
              }`}
            >
              <Icon size={17} />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="px-3 py-4 border-t border-border">
        <Link href="/settings" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-muted hover:text-text hover:bg-card transition-colors">
          <Settings size={17} />
          Settings
        </Link>
        <div className="flex items-center gap-2 mt-3 px-3">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-[11px] font-bold">GJ</div>
          <div>
            <div className="text-xs font-medium">George Jabley</div>
            <div className="text-[10px] text-muted">Demo Workspace</div>
          </div>
        </div>
        <div className="px-3 mt-3 text-[9.5px] text-muted/70">
          Built with Claude AI
        </div>
      </div>
    </aside>
  );
}
