from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    app_name: str = "ChiefFlow AI"
    environment: str = "development"
    database_url: str = "sqlite:///./chiefflow.db"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # --- AI Model Routing ---
    # Full URLs including /chat/completions - our code does not append any
    # path, it posts directly to whatever's here. A base-only URL 404s.
    gemma_api_url: str = "https://api.fireworks.ai/inference/v1/chat/completions"
    gemma_api_key: str = ""
    # Verified working: dedicated Fireworks deployment (scale-to-zero).
    # The generic catalog ID (accounts/fireworks/models/gemma-4-31b-it)
    # returns "not found/inaccessible" - it requires this deployment path.
    gemma_model: str = "accounts/techwokx-cypdje8ujre/deployments/foync9bv"

    amd_gpu_api_url: str = ""
    amd_gpu_api_key: str = ""
    amd_gpu_model: str = "NousResearch/Meta-Llama-3.1-8B-Instruct"

    fireworks_api_url: str = "https://api.fireworks.ai/inference/v1/chat/completions"
    fireworks_api_key: str = ""
    # Verified working and confirmed present in the account's model catalog.
    fireworks_model: str = "accounts/fireworks/models/gpt-oss-120b"

    upload_dir: str = "./uploads"
    cors_origins: str = "*"

    # Use SettingsConfigDict for modern Pydantic v2
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
