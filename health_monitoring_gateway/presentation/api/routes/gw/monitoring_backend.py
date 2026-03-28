"""Backend Health & Monitoring endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from health_monitoring_gateway.domain.schemas import (
    BackendHealthStatusResponse,
    BackendVersionResponse,
    JsonObjectResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["Health & Monitoring (backend)"])


@router.get("/health", response_model=BackendHealthStatusResponse)
async def backend_health():
    status, data = await request("GET", "health")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    if isinstance(data, dict):
        return BackendHealthStatusResponse.model_validate(data)
    return BackendHealthStatusResponse()


@router.get("/health/detailed")
async def backend_health_detailed():
    status, data = await request("GET", "health/detailed")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/version", response_model=BackendVersionResponse)
async def backend_version():
    status, data = await request("GET", "version")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return BackendVersionResponse.model_validate(data)


@router.post("/admin/migrate", response_model=JsonObjectResponse)
async def backend_migrate():
    status, data = await request("POST", "admin/migrate")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    if isinstance(data, dict):
        return JsonObjectResponse.model_validate(data)
    return JsonObjectResponse()


@router.post("/admin/clear-cache", response_model=JsonObjectResponse)
async def backend_clear_cache():
    status, data = await request("POST", "admin/clear-cache")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    if isinstance(data, dict):
        return JsonObjectResponse.model_validate(data)
    return JsonObjectResponse()
