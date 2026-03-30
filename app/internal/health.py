"""Gateway health check."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Gateway health - does not check downstream services."""
    return {"status": "healthy", "service": "api-gateway"}
