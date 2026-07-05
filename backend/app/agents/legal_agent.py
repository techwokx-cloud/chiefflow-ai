from app.ai import local_engine
from app.agents.base import ask_ai


async def process(text: str, sender: str | None, intent: str, tier: str) -> dict:
    entities = local_engine.extract_entities(text)
    system = (
        "You are the Legal Agent inside ChiefFlow AI. Review the contract text below and identify: "
        "key obligations, important dates, and any risk clauses. Respond in 2-4 concise sentences. "
        "You are not providing legal advice, only flagging items for human legal review."
    )
    result = await ask_ai(system, text, tier)

    return {
        "extracted_data": {**entities, "obligations_flagged": True},
        "ai_summary": local_engine.summarize(text),
        "suggested_action": "Route to Legal for review before signing",
        "draft": result.text,
        "model_used": result.model_used,
        "model_tier": result.tier_used,
        "requires_approval": True,  # contract advice is always high-risk
    }
