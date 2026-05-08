"""Operations endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    OperationCreateDTO,
    OperationResponseDTO,
    OperationUpdateDTO,
)

router = APIRouter(prefix="/v1/iam/operations", tags=["Operations"])


@router.post("/", response_model=ApiResponseSingle[OperationResponseDTO], status_code=201)
async def create_operation(payload: OperationCreateDTO):
    """Create a new operation (verb). Returns 409 if key exists."""
    status, data = await request(IAM_URL, "POST", "v1/iam/operations", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[OperationResponseDTO])
async def list_operations(
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(50, ge=1, le=200, description="Items per page."),
):
    """List all operations in the system with pagination."""
    params = {"page": page, "limit": limit}
    status, data = await request(IAM_URL, "GET", "v1/iam/operations", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_operation}", response_model=ApiResponseSingle[OperationResponseDTO])
async def get_operation(uuid_operation: str):
    """Get an operation by UUID."""
    status, data = await request(IAM_URL, "GET", f"v1/iam/operations/{uuid_operation}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_operation}", response_model=ApiResponseSingle[OperationResponseDTO])
async def update_operation(uuid_operation: str, payload: OperationUpdateDTO):
    """Update an operation name."""
    status, data = await request(
        IAM_URL, "PATCH", f"v1/iam/operations/{uuid_operation}", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_operation}", status_code=204)
async def delete_operation(uuid_operation: str):
    """Delete an operation by UUID."""
    status, data = await request(IAM_URL, "DELETE", f"v1/iam/operations/{uuid_operation}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return Response(status_code=204)