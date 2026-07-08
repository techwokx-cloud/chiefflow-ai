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
    # Set these to empty strings so they are REQUIRED from the environment
    # If they are missing, Pydantic will raise an error rather than 
    # using a faulty hardcoded URL.
    gemma_api_url: str = "https://api.fireworks.ai/inference/v1"
    gemma_api_key: str = ""
    gemma_model: str = "accounts/fireworks/models/gemma-4-31b-it"

    amd_gpu_api_url: str = ""
    amd_gpu_api_key: str = ""
    amd_gpu_model: str = "llama-3.1-8b-instruct"

    fireworks_api_url: str = "https://api.fireworks.ai/inference/v1"
    fireworks_api_key: str = ""
    fireworks_model: str = "accounts/fireworks/models/llama-v3p1-8b-instruct"

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
