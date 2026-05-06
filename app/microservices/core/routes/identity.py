"""Identity (personal identifiers) endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.core.app import CORE_URL
from app.microservices.core.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CreateIdentifierDTO,
    IdentifierResponseDTO,
    UpdateIdentifierDTO,
)

router = APIRouter(tags=["Identity"])


@router.post("/{uuid_person}/identifiers", response_model=ApiResponseSingle[IdentifierResponseDTO], status_code=201)
async def create_identifier(uuid_person: str, payload: CreateIdentifierDTO):
    """Add a personal identifier (CURP, RFC, etc.) to a person."""
    status, data = await request(CORE_URL, "POST", f"v1/people/{uuid_person}/identifiers", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}/identifiers", response_model=ApiResponsePaginated[IdentifierResponseDTO])
async def list_identifiers(
    uuid_person: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    """List all personal identifiers for a person."""
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/identifiers", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}/identifiers", response_model=ApiResponseSingle[IdentifierResponseDTO])
async def update_identifier(uuid_person: str, payload: UpdateIdentifierDTO):
    """Update a person's identifier (takes the first/single identifier)."""
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/{uuid_person}/identifiers",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_person}/identifiers", status_code=204)
async def delete_identifier(uuid_person: str):
    """Delete a person's identifier (takes the first/single identifier)."""
    status, data = await request(CORE_URL, "DELETE", f"v1/people/{uuid_person}/identifiers")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
