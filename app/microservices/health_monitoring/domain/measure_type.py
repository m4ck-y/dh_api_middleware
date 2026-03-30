"""Measure Type schemas."""

from pydantic import BaseModel


class MeasureTypeBase(BaseModel):
    name: str
    id_unit: int


class MeasureTypeCreate(MeasureTypeBase):
    pass


class MeasureTypeRead(MeasureTypeBase):
    id: int

    class Config:
        from_attributes = True
