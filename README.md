# ChiefFlow AI

**The AI Chief of Staff for Modern Businesses**
Built for AMD Developer Hackathon 2026.

ChiefFlow AI turns incoming business input — emails, PDFs, contracts, meeting notes,
support tickets — into classified, routed, human-approved workflows. A Manager Agent
detects intent and delegates to one of six specialist agents (Email, Finance, Legal,
Research, Calendar, Support), using the cheapest AI model tier capable of the job.

# ChiefFlow AI

**The AI Chief of Staff for Modern Businesses**
Built for AMD Developer Hackathon 2026.

ChiefFlow AI turns incoming business input — emails, PDFs, contracts, meeting notes,
support tickets — into classified, routed, human-approved workflows. A Manager Agent
detects intent and delegates to one of six specialist agents (Email, Finance, Legal,
Research, Calendar, Support), using the cheapest AI model tier capable of the job.

The frontend (Next.js, static export) and backend (FastAPI) ship as **one container,
one process, one port** — the API is served under `/api/*` and the built frontend is
served as static files from the same FastAPI app. This is deliberate: it fits free-tier
single-service hosting (Render, Fly.io, a single Vultr droplet) with no reverse proxy
or second service required.

## Quick Start (Docker — recommended)

```bash
cp .env.example .env   # optional — works fully offline without keys
docker compose up --build
```

Open http://localhost:8000 — the app opens straight into a pre-populated **Dashboard**,
no signup or login screen. It silently authenticates against a seeded demo workspace
on first load.

## Deploying on Render (free tier, one service)

1. Push this repo to GitHub.
2. Render → New → Web Service → connect the repo.
3. Environment: **Docker**. Root directory: repo root (the `Dockerfile` at top level
   builds both frontend and backend into one image).
4. Render sets `$PORT` automatically — the container already respects it.
5. Optionally add `GEMMA_API_KEY` / `AMD_GPU_API_KEY` / `FIREWORKS_API_KEY` as env vars
   for live model calls; leave blank to run fully on the local fallback engine.

## Demo Flow (60–90 seconds)

1. Dashboard opens — already populated with sample workflows and live analytics.
2. Drop a PDF/invoice/email text into the upload zone.
3. Watch the AI processing animation (classify → extract → summarize → route).
4. Review the extracted result: intent, assigned agent, model used, suggested action.
5. Click **Approve** — the action executes and the Activity Timeline + Analytics update instantly.

## Architecture

```
Manager Agent
 ├─ Email Agent      (replies & triage)
 ├─ Finance Agent    (invoices, amounts, due dates)
 ├─ Legal Agent      (contracts, obligations, risk)
 ├─ Research Agent   (tenders, market research)
 ├─ Calendar Agent   (scheduling, agendas)
 └─ Support Agent    (tickets, sentiment)
```

**AI Model Routing** (cost-optimized — cheapest capable model wins):

| Tier | Model | Used for |
|---|---|---|
| Simple | Gemma | Quick classification, meeting requests |
| Moderate | Open model on AMD GPU (ROCm) | Invoices, support tickets |
| Complex | Fireworks AI | Contracts, tenders |

Every tier is optional. If a provider isn't configured (no API key), the router
automatically falls back down the chain, and ultimately to a deterministic local
reasoning engine — so ChiefFlow AI is **always demoable offline**, with zero API keys.

High-risk actions (sending emails, financial approval, contract sign-off) always
require human approval before execution — see `HIGH_RISK_INTENTS` in
`backend/app/agents/base.py`.

## Tech Stack

- **Frontend:** Next.js 14 (App Router) · React · Tailwind CSS
- **Backend:** FastAPI · SQLModel (SQLite) · async agent pipeline
- **AI:** Gemma · AMD GPU (ROCm) · Fireworks AI, with local heuristic fallback
- **Deployment:** Docker Compose

## Configuring Real AI Providers

Set these in `.env` (root, used by `docker-compose.yml`) or `backend/.env`:

```
GEMMA_API_URL=https://api.fireworks.ai/inference/v1/chat/completions
GEMMA_API_KEY=...          # same key as FIREWORKS_API_KEY - Gemma is served via Fireworks (AMD-hosted)
AMD_GPU_API_URL=...        # your AMD Developer Cloud / ROCm inference endpoint
AMD_GPU_API_KEY=...
FIREWORKS_API_URL=https://api.fireworks.ai/inference/v1/chat/completions
FIREWORKS_API_KEY=...
```

All three are OpenAI-compatible `chat/completions` clients (see `backend/app/ai/providers.py`).
Per the AMD Developer Hackathon guidance, Gemma models are accessed **through Fireworks AI**
(hosted on AMD hardware) rather than Google's own API - no separate Google API key needed.

## Local Development (without Docker)

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend** — for hot-reload UI work, run the dev server on its own port. Since
production uses a static export served by FastAPI (no rewrites), point API calls at
the backend directly while developing by setting `NEXT_PUBLIC_API_BASE` (already
supported as a fallback in `lib/api.ts` if you add it), or simplest: just use
`docker compose up --build` and edit — it rebuilds the combined image.
```bash
cd frontend
npm install
npm run dev   # http://localhost:3000, static-export-only features (output:"export")
              # are ignored by `next dev`, so pages still hot-reload normally
```

## Project Structure

```
chiefflow-ai/
├── backend/
│   └── app/
│       ├── ai/            # provider clients + tiered router + local fallback engine
│       ├── agents/        # manager + 6 specialist agents
│       ├── routers/       # auth, inbox, documents, agents, analytics, activity
│       ├── services/      # document text extraction
│       ├── models.py      # SQLModel tables
│       └── main.py
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # landing page
│   │   └── (app)/               # dashboard, inbox, documents, agents, analytics, workflow/[id]
│   ├── components/
│   └── lib/
└── docker-compose.yml
```

## MVP Scope

**Built:** Auth (silent demo mode) · Dashboard · Unified Inbox · Document upload (PDF/text) ·
AI routing (3-tier + fallback) · 6 specialist agents · Human-approval workflow ·
Activity/audit log · Live analytics · Docker deployment.

**Deliberately out of scope for the hackathon MVP:** live Gmail/Outlook/Slack integrations,
multi-tenant billing, Postgres/Kubernetes/Redis — see `ChiefFlowAI_Business_Logic_Workflow.md`
for the full roadmap.
