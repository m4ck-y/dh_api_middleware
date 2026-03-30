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


@router.get("/people", response_model=ApiResponsePaginated[list[PersonRead]])
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


@router.get("/people/{person_id}", response_model=ApiResponseSingle[PersonRead])
async def get_person(person_id: int):
    """Get a person by ID."""
    status, data = await request(HEALTH_MONITORING_URL, "GET", f"people/{person_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/people", response_model=PersonRead, status_code=201)
async def create_person(payload: PersonCreate):
    """Create a new person."""
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "people", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/people/{person_id}", response_model=PersonRead)
async def update_person(person_id: int, payload: PersonCreate):
    """Update a person completely (replace all fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL, "PUT", f"people/{person_id}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/people/{person_id}", response_model=PersonRead)
async def patch_person(person_id: int, payload: PersonUpdate):
    """Update a person partially (only provided fields)."""
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"people/{person_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/people/{person_id}", response_model=MessageResponse)
async def delete_person(person_id: int):
    """Delete a person by ID."""
    status, data = await request(HEALTH_MONITORING_URL, "DELETE", f"people/{person_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
