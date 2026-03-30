"""Measurement schemas."""

from pydantic import BaseModel
from datetime import datetime


class MeasurementBase(BaseModel):
    id_person: int
    id_measure_type: int
    value: float
    notes: str | None = None
    event_at: datetime


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementRead(MeasurementBase):
    id: int

    class Config:
        from_attributes = True


class MeasurementAggregation(BaseModel):
    period: str
    count: int
    avg: float | None = None
    min: float | None = None
    max: float | None = None


class MeasureTypeStatsResponse(BaseModel):
    measure_type_id: int
    total_measurements: int
    latest_value: float | None = None
    latest_date: str | None = None
