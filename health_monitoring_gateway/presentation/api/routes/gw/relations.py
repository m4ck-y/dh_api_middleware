"""Group-Type Relations endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from health_monitoring_gateway.domain.schemas import (
    MeasureTypeGroupRelation,
    MeasureGroupRead,
    MeasureTypeRead,
    LinkTypeToGroupResponse,
    MessageResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["Group-Type Relations"])


@router.get("/measure/types-groups", response_model=list[MeasureTypeGroupRelation])
async def list_type_group_relations():
    status, data = await request("GET", "measure/types-groups")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/{type_id}/groups", response_model=list[MeasureGroupRead])
async def groups_for_type(type_id: int):
    status, data = await request("GET", f"measure/types/{type_id}/groups")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/groups/{group_id}/types", response_model=list[MeasureTypeRead])
async def types_for_group(group_id: int):
    status, data = await request("GET", f"measure/groups/{group_id}/types")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post(
    "/measure/groups/{group_id}/types/{type_id}", response_model=LinkTypeToGroupResponse
)
async def link_type_to_group(group_id: int, type_id: int):
    status, data = await request("POST", f"measure/groups/{group_id}/types/{type_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete(
    "/measure/groups/{group_id}/types/{type_id}", response_model=MessageResponse
)
async def unlink_type_from_group(group_id: int, type_id: int):
    status, data = await request("DELETE", f"measure/groups/{group_id}/types/{type_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
