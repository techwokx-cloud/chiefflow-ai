from datetime import datetime, timedelta
from app.ai import local_engine
from app.agents.base import ask_ai


def _suggest_slots(n: int = 3) -> list[str]:
    base = datetime.utcnow() + timedelta(days=1)
    slots = []
    for i in range(n):
        slot = base + timedelta(days=i, hours=(9 + i * 2) - base.hour)
        slots.append(slot.strftime("%a, %b %d - %I:%M %p UTC"))
    return slots


async def process(text: str, sender: str | None, intent: str, tier: str) -> dict:
    entities = local_engine.extract_entities(text)
    system = (
        "You are the Calendar Agent inside ChiefFlow AI. Given the meeting request below, "
        "draft a short agenda (3 bullet points max)."
    )
    result = await ask_ai(system, text, tier)
    slots = _suggest_slots()

    return {
        "extracted_data": {**entities, "suggested_slots": slots},
        "ai_summary": local_engine.summarize(text),
        "suggested_action": f"Propose time slots: {', '.join(slots)}",
        "draft": result.text,
        "model_used": result.model_used,
        "model_tier": result.tier_used,
        "requires_approval": False,
    }
