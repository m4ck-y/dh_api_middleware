"""Measurement schemas."""

from pydantic import BaseModel


class MeasurementBase(BaseModel):
    person_id: int
    measure_type_id: int
    value: float
    event_at: str


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementRead(MeasurementBase):
    id: int
    created_at: str
    updated_at: str

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
