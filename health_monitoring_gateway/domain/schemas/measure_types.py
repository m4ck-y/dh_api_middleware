from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MeasureTypeBase(BaseModel):
    name: str = Field(..., examples=["Presión Arterial"])
    id_unit: int = Field(..., examples=[1])


class MeasureTypeCreate(MeasureTypeBase):
    pass


class MeasureTypeRead(MeasureTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
