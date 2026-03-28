"""Simple HTTP client for Health Monitoring backend."""

from __future__ import annotations

import os
from typing import Any

import httpx


def get_backend_url() -> str:
    return os.environ.get(
        "HEALTH_MONITORING_BACKEND_BASE_URL",
        "http://127.0.0.1:8000/api/health-monitoring",
    ).rstrip("/")


async def request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, Any]:
    """Make request to Health Monitoring backend. Returns (status_code, response_body)."""
    base = get_backend_url()
    url = f"{base}/{path.lstrip('/')}"

    client = httpx.AsyncClient(timeout=30.0)
    try:
        resp = await client.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            headers=headers,
        )
    except httpx.RequestError as exc:
        raise ConnectionError(f"Backend unavailable: {exc}") from exc
    finally:
        await client.aclose()

    try:
        body = resp.json()
    except Exception:
        body = resp.text

    return resp.status_code, body
