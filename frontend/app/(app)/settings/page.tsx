import Topbar from "@/components/Topbar";

export default function SettingsPage() {
  return (
    <>
      <Topbar title="Settings" subtitle="Integrations and configuration." />
      <div className="p-8">
        <div className="glass rounded-card p-6 max-w-lg">
          <h2 className="text-sm font-semibold mb-4">Future Integrations</h2>
          <div className="grid grid-cols-2 gap-3 text-sm text-muted">
            {["Gmail", "Outlook", "Slack", "Microsoft Teams", "Google Calendar", "Notion", "GitHub", "Jira", "HubSpot", "Salesforce"].map((s) => (
              <div key={s} className="flex items-center justify-between bg-surface border border-border rounded-lg px-3 py-2">
                {s}<span className="text-[10px] text-muted">Coming soon</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
