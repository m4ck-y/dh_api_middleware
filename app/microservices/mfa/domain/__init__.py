"""MFA domain schemas."""

from app.shared.domain import (
    ApiResponseBase,
    ApiResponsePaginated,
    ApiResponseSingle,
    PaginationResponse,
)
from app.microservices.mfa.domain.mfa_dto import (
    CreateOtpDTO,
    OtpChallengeResponseDTO,
    VerifyOtpDTO,
    VerifyOtpResponseDTO,
)

__all__ = [
    "ApiResponseBase",
    "ApiResponsePaginated",
    "ApiResponseSingle",
    "PaginationResponse",
    "CreateOtpDTO",
    "OtpChallengeResponseDTO",
    "VerifyOtpDTO",
    "VerifyOtpResponseDTO",
]
