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
TIMEOUT = httpx.Timeout(8.0)
# Gemma runs on a scale-to-zero dedicated Fireworks deployment - the first
# request after 60+ minutes idle needs a real GPU cold-start, which
# routinely takes longer than the fast 8s timeout used for everything
# else. Give it real room rather than silently falling back on every
# first-touch request.
GEMMA_TIMEOUT = httpx.Timeout(45.0)


async def _chat(url: str, api_key: str, model: str, system: str, user: str, timeout: httpx.Timeout = TIMEOUT) -> str:
    if not url or not api_key:
        raise RuntimeError("provider not configured")

    async with httpx.AsyncClient(timeout=timeout) as client:
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
        if resp.status_code >= 400:
            # Surface the provider's actual error body (e.g. "invalid api key" vs
            # "model not found") instead of just the status code - this is what
            # gets logged by router.py when a tier falls back.
            raise RuntimeError(f"{resp.status_code} from {url}: {resp.text[:300]}")
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def _chat_gemini_native(url: str, api_key: str, model: str, system: str, user: str, timeout: httpx.Timeout = TIMEOUT) -> str:
    """
    Google's Generative Language API is NOT OpenAI-compatible:
    - endpoint is {base}/v1beta/models/{model}:generateContent?key={api_key}
    - request body uses "contents"/"parts", not OpenAI's "messages"
    - response uses "candidates"/"content"/"parts", not "choices"/"message"

    Note: Gemma models served via this API have inconsistent support for the
    separate systemInstruction field (some return 500s), so the system prompt
    is folded directly into the user content instead - the safer, more
    universally-supported shape.
    """
    base = url.rstrip("/")
    endpoint = f"{base}/v1beta/models/{model}:generateContent?key={api_key}"
    combined_text = f"{system}\n\n{user}" if system else user

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            endpoint,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": combined_text}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 600},
            },
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"{resp.status_code} from {endpoint}: {resp.text[:300]}")
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


async def call_gemma(system: str, user: str) -> str:
    url, key, model = settings.gemma_api_url, settings.gemma_api_key, settings.gemma_model
    if "generativelanguage.googleapis.com" in url:
        return await _chat_gemini_native(url, key, model, system, user, timeout=GEMMA_TIMEOUT)
    return await _chat(url, key, model, system, user, timeout=GEMMA_TIMEOUT)


async def call_amd_gpu(system: str, user: str) -> str:
    return await _chat(settings.amd_gpu_api_url, settings.amd_gpu_api_key, settings.amd_gpu_model, system, user)


async def call_fireworks(system: str, user: str) -> str:
    return await _chat(settings.fireworks_api_url, settings.fireworks_api_key, settings.fireworks_model, system, user)
