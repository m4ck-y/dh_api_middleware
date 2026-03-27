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

router = APIRouter(tags=["Measure Groups"])


@router.get("/measure/groups", response_model=list[schemas.MeasureGroupRead])
async def list_groups(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "measure/groups")
    raise_backend_http_error(status, data)
    return data


@router.get("/measure/groups/{id}", response_model=schemas.MeasureGroupRead)
async def get_group(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measure/groups/{id}")
    raise_backend_http_error(status, data)
    return data


@router.post("/measure/groups", response_model=schemas.MeasureGroupRead)
async def create_group(
    request: Request,
    payload: schemas.MeasureGroupCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        "measure/groups",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.put("/measure/groups/{id}", response_model=schemas.MeasureGroupRead)
async def update_group(
    request: Request,
    id: int,
    payload: schemas.MeasureGroupCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/groups/{id}",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.patch("/measure/groups/{id}", response_model=schemas.MeasureGroupRead)
async def patch_group(
    request: Request,
    id: int,
    payload: schemas.MeasureGroupCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/groups/{id}",
        body=payload.model_dump_json(exclude_unset=True).encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.delete("/measure/groups/{id}", response_model=schemas.MessageResponse)
async def delete_group(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measure/groups/{id}")
    raise_backend_http_error(status, data)
    return data
