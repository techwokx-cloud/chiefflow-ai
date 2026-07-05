from app.ai import local_engine
from app.agents.base import ask_ai


async def process(text: str, sender: str | None, intent: str, tier: str) -> dict:
    entities = local_engine.extract_entities(text)
    system = (
        "You are the Email Agent inside ChiefFlow AI, an AI Chief of Staff. "
        "Draft a short, professional reply to the email below. Be concise."
    )
    result = await ask_ai(system, text, tier)
    return {
        "extracted_data": {**entities, "draft_reply": local_engine.draft_reply(text, intent, sender)},
        "ai_summary": local_engine.summarize(text),
        "suggested_action": "Reply",
        "draft": result.text,
        "model_used": result.model_used,
        "model_tier": result.tier_used,
        "requires_approval": True,  # sending email is a high-risk action
    }
