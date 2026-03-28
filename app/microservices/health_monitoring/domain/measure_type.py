"""Measure Type schemas."""

from pydantic import BaseModel


class MeasureTypeBase(BaseModel):
    name: str
    description: str | None = None
    unit_id: int | None = None


class MeasureTypeCreate(MeasureTypeBase):
    pass


class MeasureTypeRead(MeasureTypeBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True
