"""Group-Type Relations endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    LinkTypeToGroupResponse,
    MeasureGroupRead,
    MeasureTypeGroupRelation,
    MeasureTypeRead,
    MessageResponse,
)

router = APIRouter(tags=["Group-Type Relations"])


@router.get("/measure/types-groups", response_model=list[MeasureTypeGroupRelation])
async def list_type_group_relations():
    status, data = await request(HEALTH_MONITORING_URL, "GET", "measure/types-groups")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/{type_id}/groups", response_model=list[MeasureGroupRead])
async def groups_for_type(type_id: int):
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measure/types/{type_id}/groups"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/groups/{group_id}/types", response_model=list[MeasureTypeRead])
async def types_for_group(group_id: int):
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measure/groups/{group_id}/types"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post(
    "/measure/groups/{group_id}/types/{type_id}", response_model=LinkTypeToGroupResponse
)
async def link_type_to_group(group_id: int, type_id: int):
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
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", f"measure/groups/{group_id}/types/{type_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
