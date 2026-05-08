"""Address endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.core.app import CORE_URL
from app.microservices.core.domain import (
    AddressResponseDTO,
    ApiResponsePaginated,
    ApiResponseSingle,
    CreateAddressDTO,
    UpdateAddressDTO,
)

router = APIRouter(prefix="/v1/people", tags=["Address"])


@router.post("/{uuid_person}/addresses", response_model=ApiResponseSingle[None], status_code=201)
async def create_address(uuid_person: str, payload: CreateAddressDTO):
    """Create an address for a person."""
    status, data = await request(CORE_URL, "POST", f"v1/people/{uuid_person}/addresses", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}/addresses", response_model=ApiResponsePaginated[AddressResponseDTO])
async def list_addresses(
    uuid_person: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    """List all addresses for a person."""
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/addresses", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/addresses/{uuid_address}", response_model=ApiResponseSingle[AddressResponseDTO])
async def get_address(uuid_address: str):
    """Get a specific address by its UUID."""
    status, data = await request(CORE_URL, "GET", f"v1/people/addresses/{uuid_address}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/addresses/{uuid_address}", response_model=ApiResponseSingle[AddressResponseDTO])
async def update_address(uuid_address: str, payload: UpdateAddressDTO):
    """Update an address by its UUID."""
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/addresses/{uuid_address}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/addresses/{uuid_address}", status_code=204)
async def delete_address(uuid_address: str):
    """Delete an address by its UUID."""
    status, data = await request(CORE_URL, "DELETE", f"v1/people/addresses/{uuid_address}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
