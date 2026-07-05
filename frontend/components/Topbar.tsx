import { Search, Bell } from "lucide-react";

export default function Topbar({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="flex items-center justify-between px-8 py-6 border-b border-border">
      <div>
        <h1 className="text-xl font-bold">{title}</h1>
        {subtitle && <p className="text-xs text-muted mt-1">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-3">
        <div className="hidden md:flex items-center gap-2 bg-surface border border-border rounded-lg px-3 py-2 w-64">
          <Search size={14} className="text-muted" />
          <input placeholder="Search workflows..." className="bg-transparent text-xs outline-none w-full placeholder:text-muted" />
        </div>
        <button className="w-9 h-9 rounded-lg bg-surface border border-border flex items-center justify-center text-muted hover:text-text">
          <Bell size={16} />
        </button>
      </div>
    </div>
  );
}
