"""Contact (email and phone) endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.core.app import CORE_URL
from app.microservices.core.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CreateEmailDTO,
    CreatePhoneDTO,
    EmailResponseDTO,
    PhoneResponseDTO,
    UpdateEmailDTO,
    UpdatePhoneDTO,
)

router = APIRouter(tags=["Contact"])


@router.post("/{uuid_person}/emails", response_model=ApiResponseSingle[EmailResponseDTO], status_code=201)
async def create_email(uuid_person: str, payload: CreateEmailDTO):
    status, data = await request(CORE_URL, "POST", f"v1/people/{uuid_person}/emails", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}/emails", response_model=ApiResponsePaginated[EmailResponseDTO])
async def list_emails(
    uuid_person: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/emails", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}/emails", response_model=ApiResponseSingle[EmailResponseDTO])
async def update_email(uuid_person: str, payload: UpdateEmailDTO):
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/{uuid_person}/emails",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_person}/emails", status_code=204)
async def delete_email(uuid_person: str):
    status, data = await request(CORE_URL, "DELETE", f"v1/people/{uuid_person}/emails")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None


@router.post("/{uuid_person}/phones", response_model=ApiResponseSingle[PhoneResponseDTO], status_code=201)
async def create_phone(uuid_person: str, payload: CreatePhoneDTO):
    status, data = await request(CORE_URL, "POST", f"v1/people/{uuid_person}/phones", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}/phones", response_model=ApiResponsePaginated[PhoneResponseDTO])
async def list_phones(
    uuid_person: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/phones", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}/phones", response_model=ApiResponseSingle[PhoneResponseDTO])
async def update_phone(uuid_person: str, payload: UpdatePhoneDTO):
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/{uuid_person}/phones",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_person}/phones", status_code=204)
async def delete_phone(uuid_person: str):
    status, data = await request(CORE_URL, "DELETE", f"v1/people/{uuid_person}/phones")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
