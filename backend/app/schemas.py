from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    org_name: str
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    org_id: str
    full_name: str


class WorkflowItemCreate(BaseModel):
    source: str
    title: str
    sender: Optional[str] = None
    raw_text: str


class WorkflowItemOut(BaseModel):
    id: str
    source: str
    title: str
    sender: Optional[str]
    intent: Optional[str]
    assigned_agent_key: Optional[str]
    priority: str
    status: str
    extracted_data: dict
    suggested_action: Optional[str]
    ai_summary: Optional[str]
    model_tier: Optional[str]
    model_used: Optional[str]
    created_at: datetime
    updated_at: datetime


class ApprovalDecision(BaseModel):
    approve: bool
    note: Optional[str] = None


class AgentOut(BaseModel):
    id: str
    key: str
    name: str
    description: str
    status: str
    accuracy: float
    tasks_handled: int
    current_task: Optional[str]


class ActivityOut(BaseModel):
    id: str
    workflow_item_id: Optional[str]
    actor: str
    action: str
    detail: str
    model_used: Optional[str]
    model_tier: Optional[str]
    created_at: datetime


class AnalyticsOut(BaseModel):
    emails_processed: int
    documents_reviewed: int
    tasks_automated: int
    hours_saved: float
    cost_saved_usd: float
    ai_accuracy: float
    approval_rate: float
    active_agents: int
    model_tier_breakdown: dict
