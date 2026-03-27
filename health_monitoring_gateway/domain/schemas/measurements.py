from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MeasurementBase(BaseModel):
    id_person: int = Field(default=1, examples=[1])
    id_measure_type: int = Field(default=1, examples=[1])
    value: float = Field(default=120.5, examples=[120.5])
    notes: Optional[str] = Field(default="Medición normal", examples=["Medición normal"])
    event_at: datetime = Field(default_factory=datetime.now)


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementRead(MeasurementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
