"""Context endpoints — aggregated IAM data for a person."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponseSingle,
    ContextResponseDTO,
)

router = APIRouter(prefix="/v1/iam", tags=["Context"])


@router.get("/context/{uuid_person}", response_model=ApiResponseSingle[ContextResponseDTO])
async def get_context(uuid_person: str):
    """
    Get aggregated IAM context (roles + permissions) for a person.

    Consumed by dh_auth during login and token refresh to inject
    authorization claims into the JWT. Returns 404 if no active
    memberships exist for the given person UUID.
    """
    status, data = await request(IAM_URL, "GET", f"v1/iam/context/{uuid_person}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data