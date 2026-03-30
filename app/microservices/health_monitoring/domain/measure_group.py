"""Measure Group schemas."""

from pydantic import BaseModel


class MeasureGroupBase(BaseModel):
    name: str
    description: str | None = None


class MeasureGroupCreate(MeasureGroupBase):
    pass


class MeasureGroupRead(MeasureGroupBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True
