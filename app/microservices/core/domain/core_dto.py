from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EAddressType(str, Enum):
    HOME = "HOME"
    WORK = "WORK"
    OTHER = "OTHER"


class EVerificationStatus(str, Enum):
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"


class EEmailType(str, Enum):
    PERSONAL = "PERSONAL"
    WORK = "WORK"
    OTHER = "OTHER"


class EPhoneType(str, Enum):
    MOBILE = "MOBILE"
    LANDLINE = "LANDLINE"
    WORK = "WORK"
    OTHER = "OTHER"


class EIdentifierType(str, Enum):
    CURP = "CURP"
    RFC = "RFC"
    NSS = "NSS"
    PASSPORT = "PASSPORT"
    OTHER = "OTHER"


class ERelationshipContact(str, Enum):
    FAMILY = "FAMILY"
    FRIEND = "FRIEND"
    WORK = "WORK"
    OTHER = "OTHER"


class CreatePersonDTO(BaseModel):
    email: str
    phone_code: str
    phone_number: str
    first_name: str
    last_name: str
    second_last_name: Optional[str] = None
    birth_date: date
    key_birth_country: str
    key_birth_state: Optional[str] = None
    type_gender: Optional[str] = None
    key_nationality: Optional[str] = None
    curp: Optional[str] = None


class PersonResponseDTO(BaseModel):
    uuid: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    type_gender: Optional[str] = None
    verification_status: EVerificationStatus


class UpdatePersonStatusDTO(BaseModel):
    verification_status: EVerificationStatus


class UpdatePersonDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    type_gender: Optional[str] = None
    verification_status: Optional[EVerificationStatus] = None


class PersonExistsResponseDTO(BaseModel):
    email_already_registered: bool = False
    personal_id_already_registered: bool = False
    phone_already_registered: bool = False


class CreateAddressDTO(BaseModel):
    postal_code: str
    key_state: str
    key_municipality: str
    key_colony: Optional[str] = None
    address: str
    address_complement: Optional[str] = None
    type_address: EAddressType = EAddressType.HOME


class UpdateAddressDTO(BaseModel):
    postal_code: Optional[str] = None
    key_state: Optional[str] = None
    key_municipality: Optional[str] = None
    key_colony: Optional[str] = None
    address: Optional[str] = None
    address_complement: Optional[str] = None
    type_address: Optional[EAddressType] = None


class AddressResponseDTO(BaseModel):
    uuid: UUID
    type_address: EAddressType
    postal_code: Optional[str] = None
    key_state: Optional[str] = None
    key_municipality: Optional[str] = None
    key_colony: Optional[str] = None
    address: Optional[str] = None
    address_complement: Optional[str] = None


class CreateEmailDTO(BaseModel):
    email: str
    type_email: EEmailType = EEmailType.PERSONAL


class EmailResponseDTO(BaseModel):
    uuid: UUID
    email: str
    type_email: EEmailType


class UpdateEmailDTO(BaseModel):
    type_email: Optional[EEmailType] = None


class CreatePhoneDTO(BaseModel):
    code: str
    number: str
    type_phone: EPhoneType = EPhoneType.MOBILE


class PhoneResponseDTO(BaseModel):
    uuid: UUID
    code: str
    number: str
    type_phone: EPhoneType


class UpdatePhoneDTO(BaseModel):
    code: Optional[str] = None
    number: Optional[str] = None
    type_phone: Optional[EPhoneType] = None


class CreateIdentifierDTO(BaseModel):
    id_identifier_type: EIdentifierType
    identifier_value: str


class IdentifierResponseDTO(BaseModel):
    uuid: UUID
    type: EIdentifierType
    value: str


class UpdateIdentifierDTO(BaseModel):
    id_identifier_type: Optional[EIdentifierType] = None
    identifier_value: Optional[str] = None


class CreateEmergencyContactDTO(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    relationship_type: ERelationshipContact
    notes: Optional[str] = None


class UpdateEmergencyContactDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    relationship_type: Optional[ERelationshipContact] = None
    notes: Optional[str] = None


class EmergencyContactResponseDTO(BaseModel):
    uuid: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    relationship_type: ERelationshipContact
    notes: Optional[str] = None
