"use client";
import { useEffect, useState, useCallback } from "react";
import Topbar from "@/components/Topbar";
import UploadDropzone from "@/components/UploadDropzone";
import WorkflowCard from "@/components/WorkflowCard";
import { api } from "@/lib/api";
import { WorkflowItem } from "@/lib/types";

export default function DocumentsPage() {
  const [items, setItems] = useState<WorkflowItem[]>([]);

  const load = useCallback(async () => {
    const all = await api.listInbox();
    setItems(all.filter((i) => ["pdf", "docx"].includes(i.source)));
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <>
      <Topbar title="Document Intelligence" subtitle="Upload contracts, invoices, and reports — ChiefFlow AI extracts what matters." />
      <div className="p-8 space-y-8">
        <UploadDropzone onDone={load} />
        <div>
          <h2 className="text-sm font-semibold mb-3 text-muted uppercase tracking-wide">Processed Documents</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {items.length === 0 && <div className="text-sm text-muted col-span-3 text-center py-12">No documents uploaded yet.</div>}
            {items.map((item) => <WorkflowCard key={item.id} item={item} />)}
          </div>
        </div>
      </div>
    </>
  );
}
