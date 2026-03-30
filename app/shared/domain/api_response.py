"""API Response schemas with pagination."""

from enum import IntEnum
from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar

T = TypeVar("T")


class InternalCode(IntEnum):
    SUCCESS = 0
    NOT_FOUND = 1
    VALIDATION_ERROR = 2
    BAD_REQUEST = 3
    UNAUTHORIZED = 4
    FORBIDDEN = 5
    SERVER_ERROR = 10
    EXTERNAL_SERVICE_ERROR = 11


class PaginationResponse(BaseModel):
    limit: int
    pages: int
    total: int
    page: int


class ApiResponseBase(BaseModel):

    status_code: int = 200
    internal_code: int | None = None
    message: str | None = None


class ApiResponseSingle(ApiResponseBase, Generic[T]):
    data: T | None = None


class ApiResponsePaginated(ApiResponseBase, Generic[T]):
    data: list[T]
    pagination: PaginationResponse
