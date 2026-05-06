"""Memberships endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    MembershipCreateDTO,
    MembershipResponseDTO,
    MembershipUpdateDTO,
)

router = APIRouter(tags=["Memberships"])


@router.post("/", response_model=ApiResponseSingle[MembershipResponseDTO], status_code=201)
async def create_membership(payload: MembershipCreateDTO):
    """Create a new membership linking a person to a tenant."""
    status, data = await request(IAM_URL, "POST", "v1/iam/memberships", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[MembershipResponseDTO])
async def list_memberships(
    uuid_person: str = Query(..., description="Filter memberships by person UUID."),
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(50, ge=1, le=200, description="Items per page."),
):
    """List all memberships for a person with pagination."""
    params = {"uuid_person": uuid_person, "page": page, "limit": limit}
    status, data = await request(IAM_URL, "GET", "v1/iam/memberships", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_membership}", response_model=ApiResponseSingle[MembershipResponseDTO])
async def get_membership(uuid_membership: str):
    """Get a membership by UUID with its roles."""
    status, data = await request(IAM_URL, "GET", f"v1/iam/memberships/{uuid_membership}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_membership}", response_model=ApiResponseSingle[MembershipResponseDTO])
async def update_membership(uuid_membership: str, payload: MembershipUpdateDTO):
    """Update membership status and/or role assignments."""
    status, data = await request(
        IAM_URL, "PATCH", f"v1/iam/memberships/{uuid_membership}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_membership}", status_code=204)
async def delete_membership(uuid_membership: str):
    """Delete a membership by UUID."""
    status, data = await request(IAM_URL, "DELETE", f"v1/iam/memberships/{uuid_membership}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return Response(status_code=204)