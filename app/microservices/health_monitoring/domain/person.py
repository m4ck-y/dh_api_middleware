"""Person schemas."""

from pydantic import BaseModel
from enum import Enum


class EVerificationStatus(str, Enum):
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"


class EGenderIdentity(str, Enum):
    NO_ESPECIFICADO = "NO_ESPECIFICADO"
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    TRANSGENERO = "TRANSGENERO"
    TRANSEXUAL = "TRANSEXUAL"
    TRAVESTI = "TRAVESTI"
    INTERSEXUAL = "INTERSEXUAL"
    OTRO = "OTRO"


class PersonBase(BaseModel):
    verification_status: EVerificationStatus
    first_name: str
    last_name: str
    second_last_name: str | None = None
    type_gender: EGenderIdentity


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    verification_status: EVerificationStatus | None = None
    first_name: str | None = None
    last_name: str | None = None
    second_last_name: str | None = None
    type_gender: EGenderIdentity | None = None


class PersonRead(PersonBase):
    id: int
    created_at: str
    updated_at: str | None = None
    deleted_at: str | None = None
    url_photo: str | None = None

    class Config:
        from_attributes = True
