"""Unit schemas."""

from pydantic import BaseModel


class UnitBase(BaseModel):
    name: str
    symbol: str


class UnitCreate(UnitBase):
    pass


class UnitRead(UnitBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True
