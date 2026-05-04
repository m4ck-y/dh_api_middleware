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

router = APIRouter(tags=["Address"])


@router.post("/{uuid_person}/address", response_model=ApiResponseSingle[None], status_code=201)
async def create_address(uuid_person: str, payload: CreateAddressDTO):
    status, data = await request(CORE_URL, "POST", f"v1/people/{uuid_person}/address", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}/address", response_model=ApiResponsePaginated[AddressResponseDTO])
async def list_addresses(
    uuid_person: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/address", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}/address", response_model=ApiResponseSingle[AddressResponseDTO])
async def update_address(uuid_person: str, payload: UpdateAddressDTO):
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/{uuid_person}/address",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_person}/address", status_code=204)
async def delete_address(uuid_person: str):
    status, data = await request(CORE_URL, "DELETE", f"v1/people/{uuid_person}/address")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
