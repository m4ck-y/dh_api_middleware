"""Waitlist proxy endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.onboarding.app import ONBOARDING_URL
from app.microservices.onboarding.domain import (
    ApiResponsePaginated,
    ApiResponseSingle,
    CheckEmailResponseDTO,
    InviteResponseDTO,
    LeadResponseDTO,
    RegisterLeadDTO,
)

router = APIRouter(tags=["Waitlist"])


@router.post("/", response_model=ApiResponseSingle[LeadResponseDTO], status_code=201)
async def register_lead(payload: RegisterLeadDTO):
    """
    Register a new lead in the waitlist.
    Returns 409 if the email is already registered.
    """
    status, data = await request(ONBOARDING_URL, "POST", "v1/waitlist", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/check/{email}", response_model=ApiResponseSingle[CheckEmailResponseDTO])
async def check_email(email: str):
    """
    Check if an email is already registered in the waitlist.
    Useful for real-time validation on landing pages before form submission.
    """
    status, data = await request(ONBOARDING_URL, "GET", f"v1/waitlist/check/{email}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/", response_model=ApiResponsePaginated[LeadResponseDTO])
async def list_leads(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by lifecycle status"),
    source: Optional[str] = Query(None, description="Filter by origin channel"),
):
    """List all waitlist leads with optional filters. Admin only."""
    params = {"page": page, "limit": limit}
    if status:
        params["status"] = status
    if source:
        params["source"] = source
    status_code, data = await request(ONBOARDING_URL, "GET", "v1/waitlist", params=params)
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data


@router.post("/{email}/invite", response_model=ApiResponseSingle[InviteResponseDTO])
async def invite_lead(email: str):
    """
    Invite a lead to start onboarding.
    Generates a secure token and sets status to INVITED.
    Returns 404 if not found, 409 if blocked or already converted.
    """
    status, data = await request(ONBOARDING_URL, "POST", f"v1/waitlist/{email}/invite")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
