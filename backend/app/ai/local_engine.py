"""
Local Reasoning Engine
=======================
Deterministic, dependency-free NLP used for:
  1. Structured extraction (dates, amounts, entities) — always run,
     regardless of which AI tier is used, because regex is cheaper
     and more reliable than an LLM for this.
  2. A full offline fallback when no AI provider is configured, so
     ChiefFlow AI is always demoable without live API keys.
"""
import re
from datetime import datetime

INTENT_KEYWORDS = {
    "invoice": ["invoice", "amount due", "payment", "bill", "remit"],
    "contract": ["contract", "agreement", "terms and conditions", "obligations", "clause"],
    "complaint": ["complaint", "unhappy", "refund", "disappointed", "not working", "issue with"],
    "tender": ["tender", "rfp", "request for proposal", "bid", "procurement"],
    "meeting": ["meeting", "schedule", "calendar", "availability", "call at"],
    "support_request": ["help", "support", "ticket", "trouble", "error", "broken"],
}

URGENT_WORDS = ["urgent", "asap", "immediately", "overdue", "critical", "emergency"]
NEGATIVE_WORDS = ["angry", "unacceptable", "disappointed", "frustrated", "terrible", "worst", "refund"]
POSITIVE_WORDS = ["thanks", "great", "appreciate", "happy", "excellent", "love"]

MONEY_RE = re.compile(r"(?:USD|GHS|\$|GH\u20b5)\s?([\d,]+(?:\.\d{2})?)", re.IGNORECASE)
DATE_RE = re.compile(
    r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?)\b",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
NAME_LINE_RE = re.compile(r"(?:from|dear|hi|hello)[:,]?\s+([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)", re.IGNORECASE)


def classify_intent(text: str) -> str:
    lower = text.lower()
    scores = {intent: sum(lower.count(kw) for kw in kws) for intent, kws in INTENT_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "other"


def priority_score(text: str) -> str:
    lower = text.lower()
    if any(w in lower for w in URGENT_WORDS):
        return "urgent"
    if any(w in lower for w in NEGATIVE_WORDS):
        return "high"
    if "?" in text and len(text) < 200:
        return "normal"
    return "normal"


def sentiment(text: str) -> str:
    lower = text.lower()
    neg = sum(lower.count(w) for w in NEGATIVE_WORDS)
    pos = sum(lower.count(w) for w in POSITIVE_WORDS)
    if neg > pos:
        return "negative"
    if pos > neg:
        return "positive"
    return "neutral"


def extract_entities(text: str) -> dict:
    amounts = MONEY_RE.findall(text)
    dates = DATE_RE.findall(text)
    emails = EMAIL_RE.findall(text)
    names = NAME_LINE_RE.findall(text)
    return {
        "amounts": amounts[:5],
        "dates": dates[:5],
        "emails": list(dict.fromkeys(emails))[:5],
        "names": list(dict.fromkeys(names))[:5],
    }


def summarize(text: str, max_sentences: int = 2) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s for s in sentences if len(s) > 3]
    if not sentences:
        return text[:160]
    return " ".join(sentences[:max_sentences])[:400]


SUGGESTED_ACTIONS = {
    "invoice": "Verify amount & due date, then route to Finance for payment approval.",
    "contract": "Flag key obligations and risks; route to Legal for review before signing.",
    "complaint": "Acknowledge immediately, assess sentiment, escalate if severity is high.",
    "tender": "Log deadline, assign research + proposal task to relevant team.",
    "meeting": "Check calendar availability and propose 3 time slots.",
    "support_request": "Retrieve relevant knowledge base article and draft a first response.",
    "other": "Summarize and route to the most relevant specialist agent for review.",
}


def suggested_action(intent: str) -> str:
    return SUGGESTED_ACTIONS.get(intent, SUGGESTED_ACTIONS["other"])


def draft_reply(text: str, intent: str, sender: str | None = None) -> str:
    greeting = f"Hi {sender.split()[0]}," if sender else "Hi,"
    body = {
        "invoice": "Thank you for sending this over. We've logged the invoice and it's now with our finance team for review. We'll confirm payment status shortly.",
        "contract": "Thanks for sharing the agreement. Our team is reviewing the terms and will follow up with any questions or next steps.",
        "complaint": "I'm sorry to hear about this experience. I've flagged it as a priority and someone from our team will follow up shortly to make it right.",
        "tender": "Thank you for the opportunity. We've logged the tender details and are preparing our submission ahead of the deadline.",
        "meeting": "Thanks for reaching out. I've checked the calendar and will send over a few available time slots shortly.",
        "support_request": "Thanks for flagging this. We've opened a support ticket and a member of our team will get back to you shortly.",
        "other": "Thanks for your message. We've logged this and will follow up shortly.",
    }.get(intent, "Thanks for your message. We've logged this and will follow up shortly.")
    return f"{greeting}\n\n{body}\n\nBest regards,\nChiefFlow AI on behalf of the team"


def respond(system: str, user: str) -> str:
    """Generic fallback used by the router when no provider is configured at all."""
    intent = classify_intent(user)
    return f"[Local reasoning] Summary: {summarize(user)} | Detected intent: {intent} | Suggested action: {suggested_action(intent)}"
