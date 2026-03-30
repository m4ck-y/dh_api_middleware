"""API Response schemas with pagination."""

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class PaginationResponse(BaseModel):
    limit: int
    pages: int
    total: int
    page: int


class ApiResponse(BaseModel, Generic[T]):
    status_code: int = 200
    internal_code: int | None = None
    message: str | None = None
    data: Optional[T] = None
    pagination: Optional[PaginationResponse] = None
