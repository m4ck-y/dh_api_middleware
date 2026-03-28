"""Shared HTTP client for microservices."""

from __future__ import annotations

from typing import Any

import httpx


async def request(
    base_url: str,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, Any]:
    """Make HTTP request to a microservice. Returns (status_code, body)."""
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                headers=headers,
            )
        except httpx.RequestError as exc:
            raise ConnectionError(f"Service unavailable: {exc}") from exc

    try:
        body = resp.json()
    except Exception:
        body = resp.text

    return resp.status_code, body
