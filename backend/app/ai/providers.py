"""
Thin OpenAI-compatible chat-completion clients for each routing tier.

Every provider is optional. If its URL/key isn't configured, or the call
fails/times out, the router (router.py) catches the exception and falls
back to the next tier, ultimately reaching the local heuristic engine.
This keeps ChiefFlow AI fully demoable without any live API keys.
"""
import httpx
from app.config import get_settings

settings = get_settings()
TIMEOUT = httpx.Timeout(20.0)


async def _chat(url: str, api_key: str, model: str, system: str, user: str) -> str:
    if not url or not api_key:
        raise RuntimeError("provider not configured")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.2,
                "max_tokens": 600,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def call_gemma(system: str, user: str) -> str:
    return await _chat(settings.gemma_api_url, settings.gemma_api_key, settings.gemma_model, system, user)


async def call_amd_gpu(system: str, user: str) -> str:
    return await _chat(settings.amd_gpu_api_url, settings.amd_gpu_api_key, settings.amd_gpu_model, system, user)


async def call_fireworks(system: str, user: str) -> str:
    return await _chat(settings.fireworks_api_url, settings.fireworks_api_key, settings.fireworks_model, system, user)
