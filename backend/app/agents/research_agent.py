from app.ai import local_engine
from app.agents.base import ask_ai


async def process(text: str, sender: str | None, intent: str, tier: str) -> dict:
    entities = local_engine.extract_entities(text)
    system = (
        "You are the Research Agent inside ChiefFlow AI. Given the tender/proposal text below, "
        "summarize the scope, deadline, and what's needed to respond competitively. Be concise."
    )
    result = await ask_ai(system, text, tier)

    return {
        "extracted_data": {**entities, "deadline": entities["dates"][0] if entities["dates"] else None},
        "ai_summary": local_engine.summarize(text),
        "suggested_action": "Assign research + proposal drafting task to the team",
        "draft": result.text,
        "model_used": result.model_used,
        "model_tier": result.tier_used,
        "requires_approval": False,
    }
