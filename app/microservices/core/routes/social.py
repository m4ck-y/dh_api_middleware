"""Social (emergency contacts) endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.core.app import CORE_URL
from app.microservices.core.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CreateEmergencyContactDTO,
    EmergencyContactResponseDTO,
    UpdateEmergencyContactDTO,
)

router = APIRouter(tags=["Social"])


@router.post("/{uuid_person}/emergency-contacts", response_model=ApiResponseSingle[EmergencyContactResponseDTO], status_code=201)
async def create_emergency_contact(uuid_person: str, payload: CreateEmergencyContactDTO):
    status, data = await request(CORE_URL, "POST", f"v1/people/{uuid_person}/emergency-contacts", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/{uuid_person}/emergency-contacts", response_model=ApiResponsePaginated[EmergencyContactResponseDTO])
async def list_emergency_contacts(
    uuid_person: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
):
    params = {"page": page, "limit": limit}
    status, data = await request(CORE_URL, "GET", f"v1/people/{uuid_person}/emergency-contacts", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/{uuid_person}/emergency-contacts", response_model=ApiResponseSingle[EmergencyContactResponseDTO])
async def update_emergency_contact(uuid_person: str, payload: UpdateEmergencyContactDTO):
    status, data = await request(
        CORE_URL, "PATCH", f"v1/people/{uuid_person}/emergency-contacts",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/{uuid_person}/emergency-contacts", status_code=204)
async def delete_emergency_contact(uuid_person: str):
    status, data = await request(CORE_URL, "DELETE", f"v1/people/{uuid_person}/emergency-contacts")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return None
