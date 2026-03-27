from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UnitBase(BaseModel):
    name: str = Field(..., max_length=50, examples=["Kilogramos"])
    symbol: Optional[str] = Field(None, max_length=10, examples=["kg"])


class UnitCreate(UnitBase):
    pass


class UnitRead(UnitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
