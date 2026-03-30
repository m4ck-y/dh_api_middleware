"""Units endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    ApiResponseSingle,
    ApiResponsePaginated,
    CountResponse,
    MessageResponse,
    UnitCreate,
    UnitRead,
)

router = APIRouter(tags=["Units"])


@router.get("/units", response_model=ApiResponsePaginated[UnitRead])
async def list_units(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    """List all units with pagination."""
    params = {"page": page, "limit": limit}
    status, data = await request(HEALTH_MONITORING_URL, "GET", "units", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/units/count", response_model=CountResponse)
async def units_count():
    """Get total count of units."""
    status, data = await request(HEALTH_MONITORING_URL, "GET", "units/count")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/units/{unit_id}", response_model=ApiResponseSingle[UnitRead])
async def get_unit(unit_id: int):
    """Get a unit by ID."""
    status, data = await request(HEALTH_MONITORING_URL, "GET", f"units/{unit_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/units", response_model=UnitRead, status_code=201)
async def create_unit(payload: UnitCreate):
    """Create a new unit."""
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "units", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/units/{unit_id}", response_model=UnitRead)
async def update_unit(unit_id: int, payload: UnitCreate):
    """Update a unit completely (replace all fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL, "PUT", f"units/{unit_id}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/units/{unit_id}", response_model=UnitRead)
async def patch_unit(unit_id: int, payload: UnitCreate):
    """Update a unit partially (only provided fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"units/{unit_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/units/{unit_id}", response_model=MessageResponse)
async def delete_unit(unit_id: int):
    """Delete a unit by ID."""
    status, data = await request(HEALTH_MONITORING_URL, "DELETE", f"units/{unit_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
