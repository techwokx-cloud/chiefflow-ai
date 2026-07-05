import { LucideIcon } from "lucide-react";

export default function StatCard({
  icon: Icon, label, value, color = "text-primary", suffix,
}: { icon: LucideIcon; label: string; value: string | number; color?: string; suffix?: string }) {
  return (
    <div className="glass rounded-card p-5 card-hover">
      <div className="flex items-center justify-between mb-3">
        <div className={`w-9 h-9 rounded-lg bg-card flex items-center justify-center ${color}`}>
          <Icon size={18} />
        </div>
      </div>
      <div className="text-2xl font-extrabold">{value}{suffix && <span className="text-sm text-muted ml-1">{suffix}</span>}</div>
      <div className="text-xs text-muted mt-1">{label}</div>
    </div>
  );
}
