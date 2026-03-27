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

router = APIRouter(tags=["People"])


@router.get("/people", response_model=list[schemas.PersonRead])
async def list_people(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "people")
    raise_backend_http_error(status, data)
    return data


@router.get("/people/count", response_model=schemas.CountResponse)
async def people_count(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "people/count")
    raise_backend_http_error(status, data)
    return data


@router.get("/people/{id}", response_model=schemas.PersonRead)
async def get_person(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"people/{id}")
    raise_backend_http_error(status, data)
    return data


@router.post("/people", response_model=schemas.PersonRead)
async def create_person(
    request: Request,
    payload: schemas.PersonCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        "people",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.put("/people/{id}", response_model=schemas.PersonRead)
async def update_person(
    request: Request,
    id: int,
    payload: schemas.PersonCreate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{id}",
        body=payload.model_dump_json().encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.patch("/people/{id}", response_model=schemas.PersonRead)
async def patch_person(
    request: Request,
    id: int,
    payload: schemas.PersonUpdate,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{id}",
        body=payload.model_dump_json(exclude_unset=True).encode(),
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.delete("/people/{id}", response_model=schemas.MessageResponse)
async def delete_person(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"people/{id}")
    raise_backend_http_error(status, data)
    return data
