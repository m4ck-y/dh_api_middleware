"""Shared domain schemas."""

from app.shared.domain.api_response import ApiResponse, PaginationResponse
from app.shared.domain.common import (
    BackendHealthStatusResponse,
    BackendVersionResponse,
    CountResponse,
    JsonObjectResponse,
    MessageResponse,
)

__all__ = [
    "ApiResponse",
    "PaginationResponse",
    "CountResponse",
    "MessageResponse",
    "BackendHealthStatusResponse",
    "BackendVersionResponse",
    "JsonObjectResponse",
]
