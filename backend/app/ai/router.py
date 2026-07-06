"""
AI Model Routing
================
Business rule (from ChiefFlowAI_Business_Logic_Workflow.md):
    "Use the lowest-cost model capable of producing acceptable quality."

Tiers, cheapest -> most capable:
    simple    -> Gemma
    moderate  -> Open model on AMD GPU (ROCm / AMD Developer Cloud)
    complex   -> Fireworks AI

Every call degrades gracefully: if a tier's provider isn't configured or
errors out, we drop to the local heuristic engine so a task is *never*
left unprocessed. Every decision is logged with the tier + model actually
used, which powers the Analytics "cost saved" and "model usage" metrics.
"""
import time
import logging
from dataclasses import dataclass
from typing import Literal

from app.ai import providers
from app.ai import local_engine

logger = logging.getLogger("chiefflow.ai_router")

Tier = Literal["simple", "moderate", "complex"]

TIER_MODEL_NAME = {
    "simple": "Gemma",
    "moderate": "Open Model (AMD GPU / ROCm)",
    "complex": "Fireworks AI",
}

# Relative cost weight per tier, used to compute "cost saved" analytics
# against an always-use-the-biggest-model baseline.
TIER_COST_WEIGHT = {"simple": 1, "moderate": 4, "complex": 12}


@dataclass
class AIResult:
    text: str
    tier_requested: Tier
    tier_used: Tier
    model_used: str
    latency_ms: int
    degraded: bool  # True if we fell back below the requested tier


async def complete(system: str, user: str, tier: Tier) -> AIResult:
    start = time.perf_counter()

    chain: list[tuple[Tier, callable]] = {
        "simple": [("simple", providers.call_gemma)],
        "moderate": [("moderate", providers.call_amd_gpu), ("simple", providers.call_gemma)],
        "complex": [
            ("complex", providers.call_fireworks),
            ("moderate", providers.call_amd_gpu),
            ("simple", providers.call_gemma),
        ],
    }[tier]

    for candidate_tier, fn in chain:
        try:
            text = await fn(system, user)
            latency = int((time.perf_counter() - start) * 1000)
            return AIResult(
                text=text,
                tier_requested=tier,
                tier_used=candidate_tier,
                model_used=TIER_MODEL_NAME[candidate_tier],
                latency_ms=latency,
                degraded=candidate_tier != tier,
            )
        except Exception as e:
            logger.warning(f"AI provider '{candidate_tier}' failed, falling back: {type(e).__name__}: {e}")
            continue

    # Nothing configured / everything failed -> deterministic local engine.
    text = local_engine.respond(system, user)
    latency = int((time.perf_counter() - start) * 1000)
    return AIResult(
        text=text,
        tier_requested=tier,
        tier_used=tier,
        model_used="ChiefFlow Local Reasoning Engine",
        latency_ms=latency,
        degraded=True,
    )
