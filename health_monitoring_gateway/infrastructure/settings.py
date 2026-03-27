"""Runtime configuration (environment)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True, slots=True)
class Settings:
    """Gateway settings loaded from the environment."""

    health_monitoring_backend_base_url: str
    gateway_listen_host: str
    gateway_listen_port: int

    @classmethod
    def from_env(cls) -> Settings:
        base = os.environ.get(
            "HEALTH_MONITORING_BACKEND_BASE_URL",
            os.environ.get(
                "HEALTH_MONITORING_UPSTREAM_BASE_URL",
                "http://127.0.0.1:8000/api/health-monitoring",
            ),
        ).rstrip("/")
        host = os.environ.get("GATEWAY_HOST", "0.0.0.0")
        port = int(os.environ.get("GATEWAY_PORT", "8080"))
        return cls(
            health_monitoring_backend_base_url=base,
            gateway_listen_host=host,
            gateway_listen_port=port,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
