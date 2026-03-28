"""Measure Type Group schemas."""

from pydantic import BaseModel


class MeasureTypeGroupRelation(BaseModel):
    measure_type_id: int
    measure_group_id: int

    class Config:
        from_attributes = True


class MeasureTypeGroupCreate(BaseModel):
    measure_type_id: int
    measure_group_id: int


class MeasureTypeGroupRead(BaseModel):
    id: int
    measure_type_id: int
    measure_group_id: int


class LinkTypeToGroupResponse(BaseModel):
    message: str
