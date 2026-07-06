"""
ChiefFlow AI - Configuration

All AI provider credentials are optional at startup. If a key is missing,
the router falls back to the next tier, and finally to a deterministic
local heuristic so the product is always demoable offline.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "ChiefFlow AI"
    environment: str = "development"
    database_url: str = "sqlite:///./chiefflow.db"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    # --- AI Model Routing (see BUSINESS_RULE: cheapest capable model wins) ---
    gemma_api_url: str = "https://api.fireworks.ai/inference/v1/chat/completions"
    gemma_api_key: str = ""
    gemma_model: str = "accounts/fireworks/models/gemma-4-31b-it"

    amd_gpu_api_url: str = ""       # Open model served on AMD Developer Cloud (ROCm)
    amd_gpu_api_key: str = ""
    amd_gpu_model: str = "llama-3.1-8b-instruct"

    fireworks_api_url: str = "https://api.fireworks.ai/inference/v1/chat/completions"
    fireworks_api_key: str = ""
    fireworks_model: str = "accounts/fireworks/models/llama-v3p1-8b-instruct"

    upload_dir: str = "./uploads"
    cors_origins: str = "*"  # comma-separated if multiple, e.g. "https://a.com,https://b.com"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
