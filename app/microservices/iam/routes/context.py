"""Context endpoints — aggregated IAM data for a person."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.iam.app import IAM_URL
from app.microservices.iam.domain import (
    ApiResponseSingle,
    ContextResponseDTO,
)

router = APIRouter(tags=["Context"])


@router.get("/context/{uuid_person}", response_model=ApiResponseSingle[ContextResponseDTO])
async def get_context(uuid_person: str):
    status, data = await request(IAM_URL, "GET", f"v1/iam/context/{uuid_person}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data