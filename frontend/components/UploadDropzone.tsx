"use client";
import { useCallback, useRef, useState } from "react";
import { UploadCloud, Loader2, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

const STEPS = ["Detecting document type...", "Extracting key details...", "Summarizing content...", "Routing to specialist agent...", "Ready"];

export default function UploadDropzone({ onDone }: { onDone?: () => void }) {
  const [dragOver, setDragOver] = useState(false);
  const [busy, setBusy] = useState(false);
  const [step, setStep] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const process = useCallback(async (file: File) => {
    setBusy(true);
    setStep(0);
    const stepTimer = setInterval(() => setStep((s) => Math.min(s + 1, STEPS.length - 1)), 550);
    try {
      const item = await api.uploadDocument(file);
      clearInterval(stepTimer);
      setStep(STEPS.length - 1);
      setTimeout(() => {
        setBusy(false);
        onDone?.();
        router.push(`/workflow?id=${item.id}`);
      }, 400);
    } catch (e) {
      clearInterval(stepTimer);
      setBusy(false);
      alert("Upload failed. Please try again.");
    }
  }, [onDone, router]);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) process(file);
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={onDrop}
      onClick={() => !busy && inputRef.current?.click()}
      className={`relative rounded-card border-2 border-dashed p-8 text-center cursor-pointer transition-colors ${
        dragOver ? "border-primary bg-primary/10" : "border-border bg-surface/40 hover:border-primary/50"
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt,.eml,.md"
        className="hidden"
        onChange={(e) => { const f = e.target.files?.[0]; if (f) process(f); }}
      />

      {!busy ? (
        <>
          <UploadCloud className="mx-auto mb-3 text-primary" size={32} />
          <div className="font-semibold text-sm mb-1">Drop a PDF, email, or document</div>
          <div className="text-xs text-muted">or click to browse — ChiefFlow AI will classify and process it automatically</div>
        </>
      ) : (
        <div className="py-2">
          {step < STEPS.length - 1 ? (
            <Loader2 className="mx-auto mb-3 text-primary animate-spin" size={28} />
          ) : (
            <CheckCircle2 className="mx-auto mb-3 text-secondary" size={28} />
          )}
          <div className="font-semibold text-sm">{STEPS[step]}</div>
          <div className="flex justify-center gap-1.5 mt-3">
            {STEPS.map((_, i) => (
              <div key={i} className={`h-1 w-8 rounded-full ${i <= step ? "bg-primary" : "bg-border"}`} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
