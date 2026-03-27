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

router = APIRouter(tags=["Measure Types"])


@router.get("/measure/types", response_model=list[schemas.MeasureTypeRead])
async def list_measure_types(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "measure/types")
    raise_backend_http_error(status, data)
    return data


@router.get("/measure/types/count", response_model=schemas.CountResponse)
async def measure_types_count(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "measure/types/count")
    raise_backend_http_error(status, data)
    return data


@router.get("/measure/types/with-data", response_model=list[schemas.MeasureTypeRead])
async def measure_types_with_data(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "measure/types/with-data")
    raise_backend_http_error(status, data)
    return data


@router.get("/measure/types/{id}", response_model=schemas.MeasureTypeRead)
async def get_measure_type(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measure/types/{id}")
    raise_backend_http_error(status, data)
    return data


@router.post("/measure/types", response_model=schemas.MeasureTypeRead)
async def create_measure_type(
    request: Request,
    payload: schemas.MeasureTypeCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        "measure/types",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.put("/measure/types/{id}", response_model=schemas.MeasureTypeRead)
async def update_measure_type(
    request: Request,
    id: int,
    payload: schemas.MeasureTypeCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/types/{id}",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.patch("/measure/types/{id}", response_model=schemas.MeasureTypeRead)
async def patch_measure_type(
    request: Request,
    id: int,
    payload: schemas.MeasureTypeCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/types/{id}",
        body=payload.model_dump_json(exclude_unset=True).encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.delete("/measure/types/{id}", response_model=schemas.MessageResponse)
async def delete_measure_type(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measure/types/{id}")
    raise_backend_http_error(status, data)
    return data
