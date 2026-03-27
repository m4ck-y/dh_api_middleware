"""Map FastAPI handlers to backend HTTP (JSON helpers for documented routes)."""

from __future__ import annotations

import json
from typing import Any

from fastapi import HTTPException, Request

from health_monitoring_gateway.application.call_health_monitoring_backend import (
    CallHealthMonitoringBackend,
)
from health_monitoring_gateway.domain.backend_http import HealthMonitoringTransportError


async def backend_json(
    request: Request,
    gateway: CallHealthMonitoringBackend,
    backend_path: str,
    *,
    body: bytes | None = None,
    json_request: bool = False,
) -> tuple[int, Any]:
    raw_query = request.scope.get("query_string", b"").decode("latin-1")
    headers = {k: v for k, v in request.headers.items()}
    if json_request:
        headers["content-type"] = "application/json"
    headers.pop("content-length", None)

    try:
        result = await gateway.execute(
            method=request.method,
            path_under_prefix=backend_path,
            raw_query=raw_query,
            headers=headers,
            body=body,
        )
    except HealthMonitoringTransportError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Health Monitoring backend unavailable: {exc}",
        ) from exc

    if not result.body:
        return result.status_code, None

    try:
        payload = json.loads(result.body)
    except json.JSONDecodeError:
        payload = result.body.decode("utf-8", errors="replace")

    return result.status_code, payload


def raise_backend_http_error(status_code: int, payload: Any) -> None:
    if status_code < 400:
        return
    detail: Any = payload
    if isinstance(payload, dict) and "detail" in payload:
        detail = payload["detail"]
    raise HTTPException(status_code=status_code, detail=detail)
