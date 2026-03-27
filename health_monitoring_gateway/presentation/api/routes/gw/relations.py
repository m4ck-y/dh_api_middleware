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

router = APIRouter(tags=["Group-Type Relations"])


@router.get(
    "/measure/types-groups",
    response_model=list[schemas.MeasureTypeGroupRelation],
)
async def list_type_group_relations(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "measure/types-groups")
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/measure/types/{id_type}/groups",
    response_model=list[schemas.MeasureGroupRead],
)
async def groups_for_type(
    request: Request,
    id_type: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, f"measure/types/{id_type}/groups")
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/measure/groups/{id_group}/types",
    response_model=list[schemas.MeasureTypeRead],
)
async def types_for_group(
    request: Request,
    id_group: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/groups/{id_group}/types",
    )
    raise_backend_http_error(status, data)
    return data


@router.post(
    "/measure/groups/{id_group}/types/{id_type}",
    response_model=schemas.LinkTypeToGroupResponse,
)
async def link_type_to_group(
    request: Request,
    id_group: int,
    id_type: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/groups/{id_group}/types/{id_type}",
    )
    raise_backend_http_error(status, data)
    return data


@router.delete(
    "/measure/groups/{id_group}/types/{id_type}",
    response_model=schemas.MessageResponse,
)
async def unlink_type_from_group(
    request: Request,
    id_group: int,
    id_type: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"measure/groups/{id_group}/types/{id_type}",
    )
    raise_backend_http_error(status, data)
    return data
