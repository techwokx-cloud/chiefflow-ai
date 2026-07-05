import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON


def uid() -> str:
    return str(uuid.uuid4())


class Organization(SQLModel, table=True):
    id: str = Field(default_factory=uid, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: str
    role: str = "owner"  # owner | admin | member
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Agent(SQLModel, table=True):
    """The Manager Agent + 6 specialist agents. Seeded on startup."""
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")
    key: str = Field(index=True)          # email | finance | legal | research | calendar | support | manager
    name: str
    description: str
    status: str = "idle"                  # idle | running | completed
    accuracy: float = 0.96
    tasks_handled: int = 0
    current_task: Optional[str] = None


class WorkflowItem(SQLModel, table=True):
    """A unit of unified-inbox input flowing through the business workflow."""
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")

    source: str                            # email | pdf | docx | notes | chat | api
    title: str
    sender: Optional[str] = None
    raw_text: str = ""

    intent: Optional[str] = None           # invoice | contract | complaint | tender | meeting | support_request | other
    assigned_agent_key: Optional[str] = None
    priority: str = "normal"               # low | normal | high | urgent
    status: str = "received"               # received | processing | needs_approval | approved | executed | archived | rejected

    extracted_data: dict = Field(default_factory=dict, sa_column=Column(JSON))
    suggested_action: Optional[str] = None
    ai_summary: Optional[str] = None
    model_tier: Optional[str] = None       # simple | moderate | complex
    model_used: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ActivityLog(SQLModel, table=True):
    """Append-only audit trail. Every agent/human action is recorded here."""
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")
    workflow_item_id: Optional[str] = Field(default=None, foreign_key="workflowitem.id")

    actor: str                             # agent key ("email") or "user:<id>" or "system"
    action: str                            # e.g. "classified_intent", "drafted_reply", "sent_email"
    detail: str = ""
    model_used: Optional[str] = None
    model_tier: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ApprovalRequest(SQLModel, table=True):
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")
    workflow_item_id: str = Field(foreign_key="workflowitem.id")
    action_summary: str
    risk_reason: str = ""
    status: str = "pending"                # pending | approved | rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


class Task(SQLModel, table=True):
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")
    workflow_item_id: Optional[str] = Field(default=None, foreign_key="workflowitem.id")
    title: str
    status: str = "open"                   # open | in_progress | done
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CalendarEvent(SQLModel, table=True):
    id: str = Field(default_factory=uid, primary_key=True)
    org_id: str = Field(foreign_key="organization.id")
    workflow_item_id: Optional[str] = Field(default=None, foreign_key="workflowitem.id")
    title: str
    start_time: datetime
    agenda: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
