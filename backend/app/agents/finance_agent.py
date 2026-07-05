from app.ai import local_engine
from app.agents.base import ask_ai


async def process(text: str, sender: str | None, intent: str, tier: str) -> dict:
    entities = local_engine.extract_entities(text)
    amount = entities["amounts"][0] if entities["amounts"] else None
    due_date = entities["dates"][0] if entities["dates"] else None

    system = (
        "You are the Finance Agent inside ChiefFlow AI. Given the invoice text below, "
        "identify the vendor, amount, due date, and flag any risk (duplicate, unusual amount, missing PO). "
        "Respond in 2-3 concise sentences."
    )
    result = await ask_ai(system, text, tier)

    risk = "Amount not detected - manual review recommended" if not amount else "No anomalies detected"
    return {
        "extracted_data": {**entities, "amount": amount, "due_date": due_date, "risk_check": risk},
        "ai_summary": local_engine.summarize(text),
        "suggested_action": f"Approve payment of {amount or 'unknown amount'} due {due_date or 'unspecified date'}",
        "draft": result.text,
        "model_used": result.model_used,
        "model_tier": result.tier_used,
        "requires_approval": True,  # financial approval is always high-risk
    }
