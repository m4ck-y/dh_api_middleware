"""Measure Groups endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    ApiResponseSingle,
    ApiResponsePaginated,
    MeasureGroupCreate,
    MeasureGroupRead,
    MessageResponse,
)

router = APIRouter(tags=["Measure Groups"])


@router.get(
    "/measure/groups", response_model=ApiResponsePaginated[list[MeasureGroupRead]]
)
async def list_measure_groups(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    """List all measure groups with pagination."""
    params = {"page": page, "limit": limit}
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", "measure/groups", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/measure/groups/{group_id}", response_model=ApiResponseSingle[MeasureGroupRead]
)
async def get_measure_group(group_id: int):
    """Get a measure group by ID."""
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measure/groups/{group_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/measure/groups", response_model=MeasureGroupRead, status_code=201)
async def create_measure_group(payload: MeasureGroupCreate):
    """Create a new measure group."""
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "measure/groups", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/measure/groups/{group_id}", response_model=MeasureGroupRead)
async def update_measure_group(group_id: int, payload: MeasureGroupCreate):
    """Update a measure group completely (replace all fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PUT",
        f"measure/groups/{group_id}",
        json=payload.model_dump(),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/measure/groups/{group_id}", response_model=MeasureGroupRead)
async def patch_measure_group(group_id: int, payload: MeasureGroupCreate):
    """Update a measure group partially (only provided fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"measure/groups/{group_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/measure/groups/{group_id}", response_model=MessageResponse)
async def delete_measure_group(group_id: int):
    """Delete a measure group by ID."""
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", f"measure/groups/{group_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
