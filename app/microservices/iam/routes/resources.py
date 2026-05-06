"""Resources endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    ResourceCreateDTO,
    ResourceResponseDTO,
    ResourceUpdateDTO,
)

router = APIRouter(tags=["Resources"])


@router.post("/", response_model=ApiResponseSingle[ResourceResponseDTO], status_code=201)
async def create_resource(payload: ResourceCreateDTO):
    """Create a new resource (functional domain). Returns 409 if key exists."""
    status, data = await request(IAM_URL, "POST", "v1/iam/resources", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[ResourceResponseDTO])
async def list_resources(
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(50, ge=1, le=200, description="Items per page."),
):
    """List all resource domains in the system with pagination."""
    params = {"page": page, "limit": limit}
    status, data = await request(IAM_URL, "GET", "v1/iam/resources", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_resource}", response_model=ApiResponseSingle[ResourceResponseDTO])
async def get_resource(uuid_resource: str):
    """Get a resource by UUID."""
    status, data = await request(IAM_URL, "GET", f"v1/iam/resources/{uuid_resource}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_resource}", response_model=ApiResponseSingle[ResourceResponseDTO])
async def update_resource(uuid_resource: str, payload: ResourceUpdateDTO):
    """Update a resource name."""
    status, data = await request(
        IAM_URL, "PATCH", f"v1/iam/resources/{uuid_resource}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_resource}", status_code=204)
async def delete_resource(uuid_resource: str):
    """Delete a resource by UUID."""
    status, data = await request(IAM_URL, "DELETE", f"v1/iam/resources/{uuid_resource}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return Response(status_code=204)