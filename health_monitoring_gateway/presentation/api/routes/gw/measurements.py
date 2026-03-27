from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Request

from health_monitoring_gateway.application.call_health_monitoring_backend import (
    CallHealthMonitoringBackend,
)
from health_monitoring_gateway.domain import schemas
from health_monitoring_gateway.presentation.api.dependencies import get_health_monitoring_backend
from health_monitoring_gateway.presentation.backend_http_bridge import (
    backend_json,
    raise_backend_http_error,
)

router = APIRouter(tags=["Measurements"])


@router.get("/measurements", response_model=list[schemas.MeasurementRead])
async def list_measurements(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    person_id: Optional[int] = Query(None),
    measure_type_id: Optional[int] = Query(None),
    event_at_gte: Optional[str] = Query(None),
    event_at_lte: Optional[str] = Query(None),
):
    status, data = await backend_json(request, backend, "measurements")
    raise_backend_http_error(status, data)
    return data


@router.get("/measurements/{id}", response_model=schemas.MeasurementRead)
async def get_measurement(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measurements/{id}")
    raise_backend_http_error(status, data)
    return data


@router.post("/measurements", response_model=schemas.MeasurementRead)
async def create_measurement(
    request: Request,
    payload: schemas.MeasurementCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        "measurements",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.put("/measurements/{id}", response_model=schemas.MeasurementRead)
async def update_measurement(
    request: Request,
    id: int,
    payload: schemas.MeasurementCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measurements/{id}",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.patch("/measurements/{id}", response_model=schemas.MeasurementRead)
async def patch_measurement(
    request: Request,
    id: int,
    payload: schemas.MeasurementCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measurements/{id}",
        body=payload.model_dump_json(exclude_unset=True).encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.delete("/measurements/{id}", response_model=schemas.MessageResponse)
async def delete_measurement(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measurements/{id}")
    raise_backend_http_error(status, data)
    return data
