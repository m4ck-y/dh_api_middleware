from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MeasureGroupBase(BaseModel):
    name: str = Field(..., max_length=100, examples=["Signos Vitales"])


class MeasureGroupCreate(MeasureGroupBase):
    pass


class MeasureGroupRead(MeasureGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
