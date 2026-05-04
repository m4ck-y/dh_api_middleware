"""Permissions endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    PermissionCreateDTO,
    PermissionResponseDTO,
)

router = APIRouter(tags=["Permissions"])


@router.post("/", response_model=ApiResponseSingle[PermissionResponseDTO], status_code=201)
async def create_permission(payload: PermissionCreateDTO):
    status, data = await request(IAM_URL, "POST", "v1/iam/permissions", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[PermissionResponseDTO])
async def list_permissions(
    active_only: bool = Query(True, description="Filter by active permissions only."),
    page: int = Query(1, ge=1, description="Page number."),
    limit: int = Query(50, ge=1, le=200, description="Items per page."),
):
    params = {"active_only": active_only, "page": page, "limit": limit}
    status, data = await request(IAM_URL, "GET", "v1/iam/permissions", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_permission}", response_model=ApiResponseSingle[PermissionResponseDTO])
async def get_permission(uuid_permission: str):
    status, data = await request(IAM_URL, "GET", f"v1/iam/permissions/{uuid_permission}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_permission}/toggle", response_model=ApiResponseSingle[PermissionResponseDTO])
async def toggle_permission(uuid_permission: str):
    status, data = await request(IAM_URL, "POST", f"v1/iam/permissions/{uuid_permission}/toggle")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_permission}", status_code=204)
async def delete_permission(uuid_permission: str):
    status, data = await request(IAM_URL, "DELETE", f"v1/iam/permissions/{uuid_permission}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return Response(status_code=204)