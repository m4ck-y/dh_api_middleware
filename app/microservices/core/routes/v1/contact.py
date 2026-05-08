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

router = APIRouter(prefix="/v1/people", tags=["Contact"])


# ── EMAILS ─────────────────────────────────────────────────────────────────────

@router.post("/{uuid_person}/emails", response_model=ApiResponseSingle[EmailResponseDTO], status_code=201)
async def create_email(uuid_person: str, payload: CreateEmailDTO):
    """Add an email to a person."""
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
    """List all emails for a person."""
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/emails", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/emails/{uuid_email}", response_model=ApiResponseSingle[EmailResponseDTO])
async def get_email(uuid_email: str):
    """Get a specific email by its UUID."""
    status, data = await request(CORE_URL, "GET", f"v1/people/emails/{uuid_email}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/emails/{uuid_email}", response_model=ApiResponseSingle[EmailResponseDTO])
async def update_email(uuid_email: str, payload: UpdateEmailDTO):
    """Update an email by its UUID."""
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/emails/{uuid_email}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/emails/{uuid_email}", status_code=204)
async def delete_email(uuid_email: str):
    """Delete an email by its UUID."""
    status, data = await request(CORE_URL, "DELETE", f"v1/people/emails/{uuid_email}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None


# ── PHONES ─────────────────────────────────────────────────────────────────────

@router.post("/{uuid_person}/phones", response_model=ApiResponseSingle[PhoneResponseDTO], status_code=201)
async def create_phone(uuid_person: str, payload: CreatePhoneDTO):
    """Add a phone to a person."""
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
    """List all phones for a person."""
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/phones", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/phones/{uuid_phone}", response_model=ApiResponseSingle[PhoneResponseDTO])
async def get_phone(uuid_phone: str):
    """Get a specific phone by its UUID."""
    status, data = await request(CORE_URL, "GET", f"v1/people/phones/{uuid_phone}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/phones/{uuid_phone}", response_model=ApiResponseSingle[PhoneResponseDTO])
async def update_phone(uuid_phone: str, payload: UpdatePhoneDTO):
    """Update a phone by its UUID."""
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/phones/{uuid_phone}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/phones/{uuid_phone}", status_code=204)
async def delete_phone(uuid_phone: str):
    """Delete a phone by its UUID."""
    status, data = await request(CORE_URL, "DELETE", f"v1/people/phones/{uuid_phone}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
