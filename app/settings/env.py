"""Environment settings for gateway."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Gateway settings loaded from environment."""

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVICE_HEALTH_MONITORING_URL: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
