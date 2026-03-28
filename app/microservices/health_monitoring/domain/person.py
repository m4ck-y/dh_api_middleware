"""Person schemas."""

from pydantic import BaseModel


class PersonBase(BaseModel):
    first_name: str
    last_name: str
    email: str | None = None
    birth_date: str | None = None
    phone: str | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    birth_date: str | None = None
    phone: str | None = None


class PersonRead(PersonBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
