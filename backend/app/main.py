from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import get_settings
from app.database import init_db
from app.routers import auth, inbox, documents, agents, analytics, activity

settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.app_name}


app.include_router(auth.router)
app.include_router(inbox.router)
app.include_router(documents.router)
app.include_router(agents.router)
app.include_router(analytics.router)
app.include_router(activity.router)

# Serve the built Next.js static export (frontend) from the same process/port.
# All /api/* routes above take priority; anything else falls through to here.
_STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(_STATIC_DIR):
    app.mount("/", StaticFiles(directory=_STATIC_DIR, html=True), name="frontend")
