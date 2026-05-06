"""People endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.core.app import CORE_URL
from app.microservices.core.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CreatePersonDTO,
    MessageResponse,
    PersonResponseDTO,
    UpdatePersonDTO,
    UpdatePersonStatusDTO,
)

router = APIRouter(tags=["People"])


@router.get("/", response_model=ApiResponsePaginated[PersonResponseDTO])
async def list_persons(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    """Retrieve a paginated list of persons."""
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", "v1/people", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}", response_model=ApiResponseSingle[PersonResponseDTO])
async def get_person(uuid_person: str):
    """Get a person by UUID. Returns 404 if not found."""
    """Get a person by UUID. Returns 404 if not found."""
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/", response_model=ApiResponseSingle[PersonResponseDTO], status_code=201)
async def create_person(payload: CreatePersonDTO):
    """Create a new person with email, phone, and optional personal identifier."""
    status, data = await request(CORE_URL, "POST", "v1/people", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}/status", response_model=ApiResponseSingle[None])
async def update_person_status(uuid_person: str, payload: UpdatePersonStatusDTO):
    """Update a person's verification status."""
    status, data = await request(CORE_URL, "PATCH", f"v1/people/{uuid_person}/status", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}", response_model=ApiResponseSingle[PersonResponseDTO])
async def update_person(uuid_person: str, payload: UpdatePersonDTO):
    """Update a person's mutable fields."""
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/{uuid_person}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_person}", status_code=204)
async def delete_person(uuid_person: str):
    """Soft-delete a person by UUID."""
    status, data = await request(CORE_URL, "DELETE", f"v1/people/{uuid_person}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
