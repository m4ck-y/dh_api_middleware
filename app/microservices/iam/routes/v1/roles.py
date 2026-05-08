"""Roles endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    RoleCreateDTO,
    RolePermissionsAssignDTO,
    RoleResponseDTO,
    RoleUpdateDTO,
)

router = APIRouter(prefix="/v1/iam/roles", tags=["Roles"])


@router.post("/", response_model=ApiResponseSingle[RoleResponseDTO], status_code=201)
async def create_role(payload: RoleCreateDTO):
    """Create a new role within a tenant. Optionally assign permissions."""
    status, data = await request(IAM_URL, "POST", "v1/iam/roles", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[RoleResponseDTO])
async def list_roles(
    uuid_tenant: str = Query(..., description="Filter roles by tenant UUID."),
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(50, ge=1, le=200, description="Items per page."),
):
    """List all roles for a given tenant with pagination."""
    params = {"uuid_tenant": uuid_tenant, "page": page, "limit": limit}
    status, data = await request(IAM_URL, "GET", "v1/iam/roles", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_role}", response_model=ApiResponseSingle[RoleResponseDTO])
async def get_role(uuid_role: str):
    """Get a role by UUID with its permissions."""
    status, data = await request(IAM_URL, "GET", f"v1/iam/roles/{uuid_role}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_role}", response_model=ApiResponseSingle[RoleResponseDTO])
async def update_role(uuid_role: str, payload: RoleUpdateDTO):
    """Update a role's name and/or description."""
    status, data = await request(
        IAM_URL, "PATCH", f"v1/iam/roles/{uuid_role}", json=payload.model_dump(exclude_unset=True)
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/{uuid_role}/permissions", response_model=ApiResponseSingle[RoleResponseDTO])
async def assign_role_permissions(uuid_role: str, payload: RolePermissionsAssignDTO):
    """Replace all permission assignments for a role using permission UUIDs."""
    status, data = await request(
        IAM_URL, "PUT", f"v1/iam/roles/{uuid_role}/permissions", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_role}", status_code=204)
async def delete_role(uuid_role: str):
    """Delete a role by UUID."""
    status, data = await request(IAM_URL, "DELETE", f"v1/iam/roles/{uuid_role}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return Response(status_code=204)