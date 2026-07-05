from app.ai import local_engine
from app.agents.base import ask_ai


async def process(text: str, sender: str | None, intent: str, tier: str) -> dict:
    entities = local_engine.extract_entities(text)
    mood = local_engine.sentiment(text)
    priority = local_engine.priority_score(text)

    system = (
        "You are the Support Agent inside ChiefFlow AI. Draft an empathetic, concise first response "
        "to the customer support message below, and note whether it needs escalation."
    )
    result = await ask_ai(system, text, tier)

    return {
        "extracted_data": {**entities, "sentiment": mood, "priority": priority},
        "ai_summary": local_engine.summarize(text),
        "suggested_action": "Escalate to human agent" if mood == "negative" and priority in ("high", "urgent") else "Send drafted response",
        "draft": result.text,
        "model_used": result.model_used,
        "model_tier": result.tier_used,
        "requires_approval": mood == "negative",
    }
