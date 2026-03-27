from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MeasurementAggregation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket: datetime
    avg_value: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    count: int = 0
    value: Optional[float] = None


class MeasurementAggregationList(BaseModel):
    aggregations: list[MeasurementAggregation]
    total: int
