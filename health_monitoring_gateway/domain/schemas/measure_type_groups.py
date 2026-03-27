from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MeasureTypeGroupBase(BaseModel):
    id_measure_type: int
    id_measure_group: int


class MeasureTypeGroupCreate(MeasureTypeGroupBase):
    pass


class MeasureTypeGroupRead(MeasureTypeGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class MeasureTypeGroupRelation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_measure_type: int
    id_measure_group: int
