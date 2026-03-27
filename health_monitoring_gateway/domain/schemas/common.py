"""Small shared response shapes used by the backend API."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CountResponse(BaseModel):
    count: int = Field(..., examples=[1250])


class MessageResponse(BaseModel):
    message: str = Field(..., examples=["deleted successfully"])


class BackendHealthStatusResponse(BaseModel):
    """Backend /health may return an empty body; middleware coerces to this shape for docs."""

    status: str = Field(default="healthy", examples=["healthy"])


class BackendVersionResponse(BaseModel):
    version: str = Field(..., examples=["v2"])


class MeasureTypeStatsResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    measure_type_id: int
    count: int
    min: float | None = None
    max: float | None = None
    avg: float | None = None
    from_date: str | None = None
    to_date: str | None = None


class LinkTypeToGroupResponse(BaseModel):
    id: int
    name: str
    created_at: datetime | None = None


class JsonObjectResponse(BaseModel):
    """Loose object for admin / migration payloads."""

    model_config = ConfigDict(extra="allow")

    message: str | None = None
