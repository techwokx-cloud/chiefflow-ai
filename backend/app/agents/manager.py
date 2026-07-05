"""
Manager Agent
=============
Implements the core "Business Workflow" from the spec:

  Receive Input -> Manager Agent -> Intent Detection -> Delegate to
  Specialist -> Generate Result -> Human Review (optional) -> Execute -> Log
"""
from sqlmodel import Session, select

from app.ai import local_engine
from app.agents.base import AGENT_REGISTRY, INTENT_AGENT_MAP, INTENT_TIER_MAP
from app.agents import email_agent, finance_agent, legal_agent, research_agent, calendar_agent, support_agent
from app.models import WorkflowItem, ActivityLog, ApprovalRequest, Agent

SPECIALISTS = {
    "email": email_agent,
    "finance": finance_agent,
    "legal": legal_agent,
    "research": research_agent,
    "calendar": calendar_agent,
    "support": support_agent,
}


def _log(session: Session, org_id: str, item_id: str, actor: str, action: str, detail: str,
          model_used: str | None = None, model_tier: str | None = None) -> None:
    session.add(ActivityLog(
        org_id=org_id, workflow_item_id=item_id, actor=actor, action=action,
        detail=detail, model_used=model_used, model_tier=model_tier,
    ))


async def process_item(session: Session, item: WorkflowItem) -> WorkflowItem:
    org_id = item.org_id
    item.status = "processing"
    _log(session, org_id, item.id, "manager", "received_input", f"Received via {item.source}: \"{item.title}\"")

    # 1. Intent detection
    intent = local_engine.classify_intent(item.raw_text)
    priority = local_engine.priority_score(item.raw_text)
    item.intent = intent
    item.priority = priority
    _log(session, org_id, item.id, "manager", "classified_intent", f"Intent: {intent} | Priority: {priority}")

    # 2. Delegate to specialist
    agent_key = INTENT_AGENT_MAP.get(intent, "email")
    tier = INTENT_TIER_MAP.get(intent, "simple")
    item.assigned_agent_key = agent_key
    _log(session, org_id, item.id, "manager", "delegated", f"Routed to {AGENT_REGISTRY[agent_key].name} (tier: {tier})")

    agent_row = session.exec(
        select(Agent).where(Agent.org_id == org_id, Agent.key == agent_key)
    ).first()
    if agent_row:
        agent_row.status = "running"
        agent_row.current_task = item.title
        session.add(agent_row)
        session.commit()

    # 3. Generate result
    result = await SPECIALISTS[agent_key].process(item.raw_text, item.sender, intent, tier)
    item.extracted_data = {**result["extracted_data"], "ai_draft": result.get("draft")}
    item.ai_summary = result["ai_summary"]
    item.suggested_action = result["suggested_action"]
    item.model_used = result["model_used"]
    item.model_tier = result["model_tier"]
    _log(
        session, org_id, item.id, agent_key, "generated_result",
        result["suggested_action"], model_used=result["model_used"], model_tier=result["model_tier"],
    )

    if agent_row:
        agent_row.status = "idle"
        agent_row.tasks_handled += 1
        agent_row.current_task = None
        session.add(agent_row)

    # 4. Human review (optional, only for high-risk actions)
    if result.get("requires_approval"):
        item.status = "needs_approval"
        approval = ApprovalRequest(
            org_id=org_id, workflow_item_id=item.id,
            action_summary=result["suggested_action"],
            risk_reason="High-impact action requires human sign-off before execution.",
        )
        session.add(approval)
        _log(session, org_id, item.id, "manager", "requested_approval", result["suggested_action"])
    else:
        item.status = "executed"
        _log(session, org_id, item.id, "manager", "executed_action", result["suggested_action"])

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


async def execute_approved(session: Session, item: WorkflowItem) -> WorkflowItem:
    item.status = "executed"
    _log(session, item.org_id, item.id, "manager", "executed_action", item.suggested_action or "Action executed after approval")
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
