"""Measure Type Group schemas."""

from pydantic import BaseModel


class MeasureTypeGroupRelation(BaseModel):
    """Schema for type-group relations list (matches backend response)."""

    id_measure_type: int
    id_measure_group: int

    class Config:
        from_attributes = True


class MeasureTypeGroupCreate(BaseModel):
    """Schema for creating type-group relation."""

    measure_type_id: int
    measure_group_id: int


class MeasureTypeGroupRead(BaseModel):
    """Schema for reading type-group relation with ID."""

    id: int
    measure_type_id: int
    measure_group_id: int


class LinkTypeToGroupResponse(BaseModel):
    """Response after linking type to group."""

    message: str
