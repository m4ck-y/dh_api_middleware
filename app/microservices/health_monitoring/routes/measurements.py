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


@router.get("/measurements", response_model=ApiResponsePaginated[list[MeasurementRead]])
async def list_measurements(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
    person_id: Optional[int] = Query(None, description="Filter by person ID"),
    measure_type_id: Optional[int] = Query(
        None, description="Filter by measure type ID"
    ),
    event_at_gte: Optional[str] = Query(None, description="Filter by event date >= "),
    event_at_lte: Optional[str] = Query(None, description="Filter by event date <="),
):
    """List all measurements with pagination and optional filters."""
    params = {"page": page, "limit": limit}
    if person_id is not None:
        params["person_id"] = person_id
    if measure_type_id is not None:
        params["measure_type_id"] = measure_type_id
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
    "/measurements/{measurement_id}", response_model=ApiResponseSingle[MeasurementRead]
)
async def get_measurement(measurement_id: int):
    """Get a measurement by ID."""
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measurements/{measurement_id}"
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


@router.put("/measurements/{measurement_id}", response_model=MeasurementRead)
async def update_measurement(measurement_id: int, payload: MeasurementCreate):
    """Update a measurement completely (replace all fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PUT",
        f"measurements/{measurement_id}",
        json=payload.model_dump(),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/measurements/{measurement_id}", response_model=MeasurementRead)
async def patch_measurement(measurement_id: int, payload: MeasurementCreate):
    """Update a measurement partially (only provided fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"measurements/{measurement_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/measurements/{measurement_id}", response_model=MessageResponse)
async def delete_measurement(measurement_id: int):
    """Delete a measurement by ID."""
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", f"measurements/{measurement_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
