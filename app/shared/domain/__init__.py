"""Shared domain schemas."""

from app.shared.domain.api_response import (
    ApiResponseBase,
    ApiResponseSingle,
    ApiResponsePaginated,
    PaginationResponse,
    InternalCode,
)
from app.shared.domain.common import (
    BackendHealthStatusResponse,
    BackendVersionResponse,
    CountResponse,
    JsonObjectResponse,
    MessageResponse,
)

__all__ = [
    "ApiResponseBase",
    "ApiResponseSingle",
    "ApiResponsePaginated",
    "PaginationResponse",
    "InternalCode",
    "CountResponse",
    "MessageResponse",
    "BackendHealthStatusResponse",
    "BackendVersionResponse",
    "JsonObjectResponse",
]
