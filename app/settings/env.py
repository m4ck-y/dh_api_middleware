"""Environment settings for gateway."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Gateway settings loaded from environment."""

    HOST: str = "[IP_ADDRESS]"
    PORT: int = 8000
    ROOT_PATH: str = "/api/middleware"
    ENVIRONMENT: str = "development"
    SERVICE_HEALTH_MONITORING_URL: str = ""
    SERVICE_LOGGER_URL: str = ""
    SERVICE_NOTIFY_URL: str = ""
    # Core services
    SERVICE_CORE_URL: str = ""
    SERVICE_AUTH_URL: str = ""
    SERVICE_IAM_URL: str = ""
    SERVICE_MFA_URL: str = ""
    SERVICE_ONBOARDING_URL: str = ""
    SERVICE_STORAGE_URL: str = ""
    SERVICE_ADMIN_URL: str = ""
    # Pending
    SERVICE_CATALOGS_URL: str = ""
    SERVICE_ORGANIZATIONS_URL: str = ""
    SERVICE_EXPEDIENT_URL: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
