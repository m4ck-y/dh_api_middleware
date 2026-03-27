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

router = APIRouter(tags=["Units"])


@router.get("/units", response_model=list[schemas.UnitRead])
async def list_units(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "units")
    raise_backend_http_error(status, data)
    return data


@router.get("/units/count", response_model=schemas.CountResponse)
async def units_count(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "units/count")
    raise_backend_http_error(status, data)
    return data


@router.get("/units/{id}", response_model=schemas.UnitRead)
async def get_unit(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"units/{id}")
    raise_backend_http_error(status, data)
    return data


@router.post("/units", response_model=schemas.UnitRead)
async def create_unit(
    request: Request,
    payload: schemas.UnitCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        "units",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.put("/units/{id}", response_model=schemas.UnitRead)
async def update_unit(
    request: Request,
    id: int,
    payload: schemas.UnitCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"units/{id}",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.patch("/units/{id}", response_model=schemas.UnitRead)
async def patch_unit(
    request: Request,
    id: int,
    payload: schemas.UnitCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"units/{id}",
        body=payload.model_dump_json(exclude_unset=True).encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.delete("/units/{id}", response_model=schemas.MessageResponse)
async def delete_unit(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"units/{id}")
    raise_backend_http_error(status, data)
    return data
