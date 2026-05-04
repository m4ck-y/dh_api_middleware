"""OTP challenge endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.mfa.app import MFA_URL
from app.microservices.mfa.domain import (
    ApiResponseSingle,
    CreateOtpDTO,
    OtpChallengeResponseDTO,
    VerifyOtpDTO,
    VerifyOtpResponseDTO,
)

router = APIRouter(tags=["OTP"])


@router.post("/challenges", response_model=ApiResponseSingle[OtpChallengeResponseDTO], status_code=201)
async def create_challenge(payload: CreateOtpDTO):
    status, data = await request(MFA_URL, "POST", "v1/otp/challenges", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/challenges/{uuid_challenge}/verify", response_model=ApiResponseSingle[VerifyOtpResponseDTO])
async def verify_challenge(uuid_challenge: str, payload: VerifyOtpDTO):
    status, data = await request(MFA_URL, "POST", f"v1/otp/challenges/{uuid_challenge}/verify", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/challenges/{uuid_challenge}/resend", response_model=ApiResponseSingle[OtpChallengeResponseDTO])
async def resend_challenge(uuid_challenge: str):
    status, data = await request(MFA_URL, "POST", f"v1/otp/challenges/{uuid_challenge}/resend")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
