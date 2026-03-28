"""Measure Groups endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from health_monitoring_gateway.domain.schemas import (
    MeasureGroupCreate,
    MeasureGroupRead,
    MessageResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["Measure Groups"])


@router.get("/measure/groups", response_model=list[MeasureGroupRead])
async def list_measure_groups():
    status, data = await request("GET", "measure/groups")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/groups/{group_id}", response_model=MeasureGroupRead)
async def get_measure_group(group_id: int):
    status, data = await request("GET", f"measure/groups/{group_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/measure/groups", response_model=MeasureGroupRead, status_code=201)
async def create_measure_group(payload: MeasureGroupCreate):
    status, data = await request("POST", "measure/groups", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/measure/groups/{group_id}", response_model=MeasureGroupRead)
async def update_measure_group(group_id: int, payload: MeasureGroupCreate):
    status, data = await request(
        "PUT", f"measure/groups/{group_id}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/measure/groups/{group_id}", response_model=MeasureGroupRead)
async def patch_measure_group(group_id: int, payload: MeasureGroupCreate):
    status, data = await request(
        "PATCH",
        f"measure/groups/{group_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/measure/groups/{group_id}", response_model=MessageResponse)
async def delete_measure_group(group_id: int):
    status, data = await request("DELETE", f"measure/groups/{group_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
