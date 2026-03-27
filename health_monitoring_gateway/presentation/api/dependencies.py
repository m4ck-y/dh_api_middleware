"""FastAPI dependencies."""

from __future__ import annotations

from fastapi import Request

from health_monitoring_gateway.application.call_health_monitoring_backend import (
    CallHealthMonitoringBackend,
)


def get_health_monitoring_backend(request: Request) -> CallHealthMonitoringBackend:
    return CallHealthMonitoringBackend(request.app.state.health_monitoring_backend)
