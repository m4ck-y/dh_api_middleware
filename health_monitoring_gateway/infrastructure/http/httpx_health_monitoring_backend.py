"""httpx implementation of HealthMonitoringBackendPort."""

from __future__ import annotations

from typing import Mapping

import httpx

from health_monitoring_gateway.domain.backend_http import (
    BackendHttpResponse,
    HealthMonitoringTransportError,
)
from health_monitoring_gateway.infrastructure.http.header_policy import (
    filter_request_headers,
    filter_response_headers,
)
from health_monitoring_gateway.infrastructure.settings import Settings


class HttpxHealthMonitoringBackend:
    """Performs HTTP calls to the Health Monitoring service."""

    def __init__(self, *, settings: Settings, client: httpx.AsyncClient) -> None:
        self._base = settings.health_monitoring_backend_base_url.rstrip("/")
        self._client = client

    async def execute_http(
        self,
        *,
        method: str,
        path: str,
        raw_query: str,
        headers: Mapping[str, str],
        body: bytes | None,
    ) -> BackendHttpResponse:
        path = path.lstrip("/")
        url = f"{self._base}/{path}" if path else self._base
        if raw_query:
            url = f"{url}?{raw_query}"

        safe_headers = filter_request_headers(dict(headers))
        try:
            resp = await self._client.request(
                method,
                url,
                headers=safe_headers,
                content=body if body else None,
            )
        except httpx.RequestError as exc:
            raise HealthMonitoringTransportError(str(exc)) from exc

        out_headers = filter_response_headers(
            {k: v for k, v in resp.headers.items()},
        )
        return BackendHttpResponse(
            status_code=resp.status_code,
            headers=out_headers,
            body=resp.content,
        )