"""Measurements endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    MeasurementCreate,
    MeasurementRead,
    MessageResponse,
)

router = APIRouter(tags=["Measurements"])


@router.get("/measurements", response_model=ApiResponsePaginated[MeasurementRead])
async def list_measurements(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
    uuid_person: Optional[str] = Query(None, description="Filter by person UUID"),
    uuid_measure_type: Optional[str] = Query(
        None, description="Filter by measure type UUID"
    ),
    event_at_gte: Optional[str] = Query(None, description="Filter by event date >= "),
    event_at_lte: Optional[str] = Query(None, description="Filter by event date <="),
):
    """List all measurements with pagination and optional filters."""
    params = {"page": page, "limit": limit}
    if uuid_person is not None:
        params["uuid_person"] = uuid_person
    if uuid_measure_type is not None:
        params["uuid_measure_type"] = uuid_measure_type
    if event_at_gte:
        params["event_at_gte"] = event_at_gte
    if event_at_lte:
        params["event_at_lte"] = event_at_lte

    status, data = await request(
        HEALTH_MONITORING_URL, "GET", "measurements", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/measurements/{uuid_measurement}", response_model=ApiResponseSingle[MeasurementRead]
)
async def get_measurement(uuid_measurement: str):
    """Get a measurement by UUID."""
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measurements/{uuid_measurement}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/measurements", response_model=MeasurementRead, status_code=201)
async def create_measurement(payload: MeasurementCreate):
    """Create a new measurement."""
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "measurements", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/measurements/{uuid_measurement}", response_model=MeasurementRead)
async def update_measurement(uuid_measurement: str, payload: MeasurementCreate):
    """Update a measurement completely (replace all fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PUT",
        f"measurements/{uuid_measurement}",
        json=payload.model_dump(),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/measurements/{uuid_measurement}", response_model=MeasurementRead)
async def patch_measurement(uuid_measurement: str, payload: MeasurementCreate):
    """Update a measurement partially (only provided fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"measurements/{uuid_measurement}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/measurements/{uuid_measurement}", response_model=MessageResponse)
async def delete_measurement(uuid_measurement: str):
    """Delete a measurement by UUID."""
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", f"measurements/{uuid_measurement}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
