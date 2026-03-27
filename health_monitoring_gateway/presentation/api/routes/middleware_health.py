"""Middleware process health only — does not call Health Monitoring."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Middleware Health"])


@router.get(
    "/health",
    summary="Gateway liveness",
    description="Indicates this middleware process is running. Does not call the Health Monitoring backend.",
)
def gateway_health() -> dict[str, str]:
    return {"status": "healthy", "service": "api-middleware"}
