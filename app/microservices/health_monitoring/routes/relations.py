"""Group-Type Relations endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    ApiResponseSingle,
    ApiResponsePaginated,
    LinkTypeToGroupResponse,
    MeasureGroupRead,
    MeasureTypeGroupRelation,
    MeasureTypeRead,
    MessageResponse,
)

router = APIRouter(tags=["Group-Type Relations"])


@router.get(
    "/measure/types-groups",
    response_model=ApiResponsePaginated[list[MeasureTypeGroupRelation]],
)
async def list_type_group_relations(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    """List all relations between measure types and groups."""
    params = {"page": page, "limit": limit}
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", "measure/types-groups", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/measure/types/{type_id}/groups",
    response_model=ApiResponsePaginated[list[MeasureGroupRead]],
)
async def groups_for_type(
    type_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    """List all groups associated with a specific measure type."""
    params = {"page": page, "limit": limit}
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measure/types/{type_id}/groups", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/measure/groups/{group_id}/types",
    response_model=ApiResponsePaginated[list[MeasureTypeRead]],
)
async def types_for_group(
    group_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    """List all measure types associated with a specific group."""
    params = {"page": page, "limit": limit}
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measure/groups/{group_id}/types", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post(
    "/measure/groups/{group_id}/types/{type_id}", response_model=LinkTypeToGroupResponse
)
async def link_type_to_group(group_id: int, type_id: int):
    """Link a measure type to a measure group."""
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", f"measure/groups/{group_id}/types/{type_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete(
    "/measure/groups/{group_id}/types/{type_id}", response_model=MessageResponse
)
async def unlink_type_from_group(group_id: int, type_id: int):
    """Unlink a measure type from a measure group."""
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", f"measure/groups/{group_id}/types/{type_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
