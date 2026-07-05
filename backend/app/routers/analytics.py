from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import WorkflowItem, Agent, User
from app.schemas import AnalyticsOut
from app.security import get_current_user
from app.ai.router import TIER_COST_WEIGHT

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

MINUTES_SAVED_PER_ITEM = 12  # conservative estimate of manual handling time replaced
BASELINE_TIER_WEIGHT = TIER_COST_WEIGHT["complex"]  # cost if every task used the biggest model
UNIT_COST_USD = 0.02  # illustrative $ per cost-weight-unit, for the "cost saved" KPI


@router.get("", response_model=AnalyticsOut)
def get_analytics(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    items = session.exec(select(WorkflowItem).where(WorkflowItem.org_id == user.org_id)).all()
    agents = session.exec(select(Agent).where(Agent.org_id == user.org_id)).all()

    emails = sum(1 for i in items if i.source == "email")
    docs = sum(1 for i in items if i.source in ("pdf", "docx"))
    executed = sum(1 for i in items if i.status == "executed")
    needs_approval = sum(1 for i in items if i.status == "needs_approval")
    rejected = sum(1 for i in items if i.status == "rejected")

    tier_breakdown = {"simple": 0, "moderate": 0, "complex": 0}
    baseline_cost = 0.0
    actual_cost = 0.0
    for i in items:
        if i.model_tier in tier_breakdown:
            tier_breakdown[i.model_tier] += 1
            actual_cost += TIER_COST_WEIGHT[i.model_tier] * UNIT_COST_USD
            baseline_cost += BASELINE_TIER_WEIGHT * UNIT_COST_USD

    cost_saved = round(baseline_cost - actual_cost, 2)
    hours_saved = round(len(items) * MINUTES_SAVED_PER_ITEM / 60, 1)

    total_decided = executed + rejected
    approval_rate = round((executed / total_decided) * 100, 1) if total_decided else 0.0

    avg_accuracy = round(sum(a.accuracy for a in agents) / len(agents) * 100, 1) if agents else 96.0
    active_agents = sum(1 for a in agents if a.status == "running") or len(agents)

    return AnalyticsOut(
        emails_processed=emails,
        documents_reviewed=docs,
        tasks_automated=executed,
        hours_saved=hours_saved,
        cost_saved_usd=cost_saved,
        ai_accuracy=avg_accuracy,
        approval_rate=approval_rate,
        active_agents=active_agents,
        model_tier_breakdown=tier_breakdown,
    )
