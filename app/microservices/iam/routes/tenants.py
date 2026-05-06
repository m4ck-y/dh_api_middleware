"""Tenants endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    TenantCreateDTO,
    TenantResponseDTO,
    TenantUpdateDTO,
)

router = APIRouter(tags=["Tenants"])


@router.post("/", response_model=ApiResponseSingle[TenantResponseDTO], status_code=201)
async def create_tenant(payload: TenantCreateDTO):
    """Create a new tenant. Returns 409 if the key already exists."""
    status, data = await request(IAM_URL, "POST", "v1/iam/tenants", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[TenantResponseDTO])
async def list_tenants(
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(50, ge=1, le=200, description="Items per page."),
):
    """List all tenants in the system with pagination."""
    params = {"page": page, "limit": limit}
    status, data = await request(IAM_URL, "GET", "v1/iam/tenants", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_tenant}", response_model=ApiResponseSingle[TenantResponseDTO])
async def get_tenant(uuid_tenant: str):
    """Get a tenant by UUID. Returns 404 if not found."""
    status, data = await request(IAM_URL, "GET", f"v1/iam/tenants/{uuid_tenant}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_tenant}", response_model=ApiResponseSingle[TenantResponseDTO])
async def update_tenant(uuid_tenant: str, payload: TenantUpdateDTO):
    """Update a tenant's mutable fields (name, description)."""
    status, data = await request(
        IAM_URL, "PATCH", f"v1/iam/tenants/{uuid_tenant}", json=payload.model_dump(exclude_unset=True)
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_tenant}", status_code=204)
async def delete_tenant(uuid_tenant: str):
    """Delete a tenant by UUID."""
    status, data = await request(IAM_URL, "DELETE", f"v1/iam/tenants/{uuid_tenant}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return Response(status_code=204)