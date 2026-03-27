from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from health_monitoring_gateway.application.call_health_monitoring_backend import (
    CallHealthMonitoringBackend,
)
from health_monitoring_gateway.domain import schemas
from health_monitoring_gateway.presentation.api.dependencies import get_health_monitoring_backend
from health_monitoring_gateway.presentation.backend_http_bridge import (
    backend_json,
    raise_backend_http_error,
)

router = APIRouter(tags=["Health & Monitoring (backend)"])


@router.get("/health", response_model=schemas.BackendHealthStatusResponse)
async def backend_health(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "health")
    raise_backend_http_error(status, data)
    if isinstance(data, dict):
        return schemas.BackendHealthStatusResponse.model_validate(data)
    return schemas.BackendHealthStatusResponse()


@router.get("/health/detailed")
async def backend_health_detailed(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "health/detailed")
    raise_backend_http_error(status, data)
    return data


@router.get("/version", response_model=schemas.BackendVersionResponse)
async def backend_version(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "version")
    raise_backend_http_error(status, data)
    return schemas.BackendVersionResponse.model_validate(data)


@router.post("/admin/migrate", response_model=schemas.JsonObjectResponse)
async def backend_migrate(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "admin/migrate")
    raise_backend_http_error(status, data)
    if isinstance(data, dict):
        return schemas.JsonObjectResponse.model_validate(data)
    return schemas.JsonObjectResponse()


@router.post("/admin/clear-cache", response_model=schemas.JsonObjectResponse)
async def backend_clear_cache(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "admin/clear-cache")
    raise_backend_http_error(status, data)
    if isinstance(data, dict):
        return schemas.JsonObjectResponse.model_validate(data)
    return schemas.JsonObjectResponse()
