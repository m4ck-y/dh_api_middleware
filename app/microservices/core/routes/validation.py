"""Validation (check-exists) endpoint."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.core.app import CORE_URL
from app.microservices.core.domain import (
    ApiResponseSingle,
    PersonExistsResponseDTO,
)

router = APIRouter(tags=["Validation"])


@router.get("/check-exists", response_model=ApiResponseSingle[PersonExistsResponseDTO])
async def check_person_exists(
    email: Optional[str] = Query(None, description="Email address to check"),
    personal_id: Optional[str] = Query(None, description="Personal identifier to check (CURP, NSS, fiscal number)"),
    phone_code: Optional[str] = Query(None, description="Phone country code"),
    phone_number: Optional[str] = Query(None, description="Phone number"),
):
    """Check which registration fields are already in use. UUIDs are logged internally — never returned."""
    params = {}
    if email:
        params["email"] = email
    if personal_id:
        params["personal_id"] = personal_id
    if phone_code:
        params["phone_code"] = phone_code
    if phone_number:
        params["phone_number"] = phone_number
    status, data = await request(CORE_URL, "GET", "v1/people/check-exists", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
