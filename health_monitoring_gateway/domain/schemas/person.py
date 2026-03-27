from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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
    second_last_name: Optional[str] = None
    type_gender: EGenderIdentity


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    verification_status: Optional[EVerificationStatus] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    type_gender: Optional[EGenderIdentity] = None


class PersonRead(PersonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    url_photo: Optional[str] = None
