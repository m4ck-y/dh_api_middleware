"""Application: invoke Health Monitoring over HTTP (method allowlist + path normalization)."""

from __future__ import annotations

from typing import Mapping

from health_monitoring_gateway.domain.backend_http import (
    BackendHttpResponse,
    HealthMonitoringBackendPort,
)


class BackendHttpMethodNotAllowedError(ValueError):
    """Raised when the HTTP method is not allowed toward the backend."""


_ALLOWED = frozenset(
    {"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
)


class CallHealthMonitoringBackend:
    """Orchestrates backend HTTP calls without transport details."""

    def __init__(self, backend: HealthMonitoringBackendPort) -> None:
        self._backend = backend

    async def execute(
        self,
        *,
        method: str,
        path_under_prefix: str,
        raw_query: str,
        headers: Mapping[str, str],
        body: bytes | None,
    ) -> BackendHttpResponse:
        if method.upper() not in _ALLOWED:
            raise BackendHttpMethodNotAllowedError(method)
        normalized = path_under_prefix.lstrip("/")
        return await self._backend.execute_http(
            method=method.upper(),
            path=normalized,
            raw_query=raw_query,
            headers=headers,
            body=body,
        )
