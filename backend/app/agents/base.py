from dataclasses import dataclass
from app.ai.router import complete, AIResult


@dataclass
class AgentMeta:
    key: str
    name: str
    description: str


AGENT_REGISTRY: dict[str, AgentMeta] = {
    "manager": AgentMeta("manager", "Manager Agent", "Classifies intent, routes work, monitors execution, requests approval."),
    "email": AgentMeta("email", "Email Agent", "Smart replies & triage."),
    "finance": AgentMeta("finance", "Finance Agent", "Review invoices & expenses."),
    "legal": AgentMeta("legal", "Legal Agent", "Contracts & compliance."),
    "research": AgentMeta("research", "Research Agent", "Market research & insights."),
    "calendar": AgentMeta("calendar", "Calendar Agent", "Scheduling & meetings."),
    "support": AgentMeta("support", "Support Agent", "Customer support & tickets."),
}

# Intent -> specialist agent
INTENT_AGENT_MAP = {
    "invoice": "finance",
    "contract": "legal",
    "complaint": "support",
    "tender": "research",
    "meeting": "calendar",
    "support_request": "support",
    "other": "email",
}

# Business rule: cheapest capable model per intent (see AI Model Routing spec)
INTENT_TIER_MAP = {
    "invoice": "moderate",
    "contract": "complex",
    "complaint": "moderate",
    "tender": "complex",
    "meeting": "simple",
    "support_request": "moderate",
    "other": "simple",
}

# Actions that always require human approval before execution
HIGH_RISK_INTENTS = {"contract", "invoice"}
HIGH_RISK_ACTION_WORDS = ("send", "pay", "delete", "escalate", "sign")


async def ask_ai(system: str, user: str, tier: str) -> AIResult:
    return await complete(system, user, tier)
