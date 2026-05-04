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
    uuid_person: str
    channel: EOtpChannel
    purpose: EOtpPurpose
    destination: str


class VerifyOtpDTO(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)


class OtpChallengeResponseDTO(BaseModel):
    uuid_challenge: str
    channel: EOtpChannel
    destination_masked: str
    expires_in_minutes: int
    status: EOtpStatus


class VerifyOtpResponseDTO(BaseModel):
    status: EOtpStatus
    message: str
    verify_attempts_remaining: Optional[int] = None
