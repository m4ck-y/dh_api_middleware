"""People endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CountResponse,
    MessageResponse,
    PersonCreate,
    PersonRead,
    PersonUpdate,
)

router = APIRouter(tags=["People"])


@router.get("/people", response_model=ApiResponsePaginated[PersonRead])
async def list_people(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=100, description="Items per page"),
):
    """List all people with pagination."""
    params = {"page": page, "limit": limit}
    status, data = await request(HEALTH_MONITORING_URL, "GET", "people", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/count", response_model=CountResponse)
async def people_count():
    """Get total count of people."""
    status, data = await request(HEALTH_MONITORING_URL, "GET", "people/count")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/{uuid_person}", response_model=ApiResponseSingle[PersonRead])
async def get_person(uuid_person: str):
    """Get a person by UUID."""
    status, data = await request(HEALTH_MONITORING_URL, "GET", f"people/{uuid_person}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/people/{uuid_person}", response_model=PersonRead)
async def update_person(uuid_person: str, payload: PersonCreate):
    """Update a person completely (replace all fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL, "PUT", f"people/{uuid_person}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/people/{uuid_person}", response_model=PersonRead)
async def patch_person(uuid_person: str, payload: PersonUpdate):
    """Update a person partially (only provided fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"people/{uuid_person}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/people/{uuid_person}", response_model=MessageResponse)
async def delete_person(uuid_person: str):
    """Delete a person by UUID."""
    status, data = await request(HEALTH_MONITORING_URL, "DELETE", f"people/{uuid_person}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
