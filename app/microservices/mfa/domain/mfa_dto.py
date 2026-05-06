from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EOtpChannel(str, Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    TOTP = "TOTP"


class EOtpPurpose(str, Enum):
    LOGIN = "LOGIN"
    RESET_PASSWORD = "RESET_PASSWORD"
    SENSITIVE_ACTION = "SENSITIVE_ACTION"
    ONBOARDING = "ONBOARDING"


class EOtpStatus(str, Enum):
    CREATED = "CREATED"
    EXPIRED = "EXPIRED"
    CONSUMED = "CONSUMED"
    BLOCKED = "BLOCKED"


class CreateOtpDTO(BaseModel):
    uuid_person: str = Field(..., description="UUID of the person (people.person.uuid).", examples=["550e8400-e29b-41d4-a716-446655440000"])
    channel: EOtpChannel = Field(..., description="Delivery channel.", examples=["EMAIL"])
    purpose: EOtpPurpose = Field(..., description="Purpose of the OTP challenge.", examples=["ONBOARDING"])
    destination: str = Field(..., description="Email address or phone number.", examples=["juan@example.com"])


class VerifyOtpDTO(BaseModel):
    code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code.", examples=["123456"])


class OtpChallengeResponseDTO(BaseModel):
    uuid_challenge: str = Field(..., description="MongoDB document ID of the challenge.", examples=["64f1a2b3c4d5e6f7a8b9c0d1"])
    channel: EOtpChannel
    destination_masked: str = Field(..., description="Masked destination for display.", examples=["j***@example.com"])
    expires_in_minutes: int = Field(..., examples=[10])
    status: EOtpStatus


class VerifyOtpResponseDTO(BaseModel):
    status: EOtpStatus = Field(..., description="Result status after verification attempt.")
    message: str = Field(..., examples=["OTP verified successfully."])
    verify_attempts_remaining: Optional[int] = Field(None, description="Remaining attempts before BLOCKED.")
