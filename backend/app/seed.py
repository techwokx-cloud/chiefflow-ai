from sqlmodel import Session, select

from app.models import Agent, WorkflowItem
from app.agents.base import AGENT_REGISTRY
from app.agents.manager import process_item, execute_approved

SPECIALIST_KEYS = [k for k in AGENT_REGISTRY if k != "manager"]

DEMO_ITEMS = [
    dict(
        source="email", title="Invoice from Acme Corp requires review", sender="billing@acmecorp.com",
        raw_text=(
            "Hi, please find attached invoice INV-2291 from Acme Corp for consulting services rendered in June. "
            "Amount due: $4,250.00 USD. Due date: July 15 2026. Kindly process payment at your earliest convenience."
        ),
    ),
    dict(
        source="pdf", title="Vendor Services Agreement - Draft", sender="legal@partnerfirm.com",
        raw_text=(
            "This Services Agreement is entered into between TechWokx IT Solutions and Partner Firm Ltd. "
            "The vendor shall deliver services by August 1 2026. Either party may terminate with 30 days notice. "
            "Client shall pay a monthly retainer of $1,200.00. Confidentiality obligations survive termination."
        ),
    ),
    dict(
        source="chat", title="Meeting request from Marketing team", sender="jane.cooper@company.com",
        raw_text="Hi, can we schedule a call to discuss the Q3 marketing plan sometime next week? Should take about 30 minutes.",
    ),
    dict(
        source="email", title="Customer complaint - order delayed", sender="frustrated.customer@gmail.com",
        raw_text=(
            "This is unacceptable. My order #5521 was supposed to arrive last week and I still haven't received it. "
            "I am extremely disappointed and want a refund immediately if this isn't resolved today."
        ),
    ),
    dict(
        source="api", title="Tender: Government IT Infrastructure Upgrade", sender="procurement@ghsrv.gov",
        raw_text=(
            "Request for Proposal: IT Infrastructure Upgrade Tender. Submission deadline: August 20 2026. "
            "Vendors must demonstrate experience with cloud migration and network security compliance."
        ),
    ),
    dict(
        source="chat", title="Support ticket - login issue", sender="user492@client.com",
        raw_text="Hi, I'm getting an error when I try to log in to my account. It just says 'something went wrong'. Can someone help?",
    ),
]


def seed_agents_for_org(session: Session, org_id: str) -> None:
    for key in SPECIALIST_KEYS:
        meta = AGENT_REGISTRY[key]
        session.add(Agent(org_id=org_id, key=key, name=meta.name, description=meta.description))
    session.commit()


async def seed_demo_workflow_items(session: Session, org_id: str) -> None:
    existing = session.exec(select(WorkflowItem).where(WorkflowItem.org_id == org_id)).first()
    if existing:
        return
    for idx, d in enumerate(DEMO_ITEMS):
        item = WorkflowItem(org_id=org_id, **d)
        session.add(item)
        session.commit()
        session.refresh(item)
        item = await process_item(session, item)
        # Auto-approve every other high-risk item so the dashboard shows a realistic
        # mix of Completed / Needs Approval, not everything stuck pending.
        if item.status == "needs_approval" and idx % 2 == 0:
            await execute_approved(session, item)
