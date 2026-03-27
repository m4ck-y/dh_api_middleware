"""HTTP contract to the Health Monitoring backend (domain: no I/O)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol


class HealthMonitoringTransportError(RuntimeError):
    """Raised when the Health Monitoring HTTP backend cannot be reached or fails at transport level."""



@dataclass(frozen=True, slots=True)
class BackendHttpResponse:
    """Normalized HTTP response from Health Monitoring for the presentation layer."""

    status_code: int
    headers: Mapping[str, str]
    body: bytes


class HealthMonitoringBackendPort(Protocol):
    """Outbound port: execute an HTTP-equivalent call against Health Monitoring."""

    async def execute_http(
        self,
        *,
        method: str,
        path: str,
        raw_query: str,
        headers: Mapping[str, str],
        body: bytes | None,
    ) -> BackendHttpResponse:
        """Path is relative to the backend API base (no leading slash required)."""
        ...
