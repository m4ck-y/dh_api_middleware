from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EOtpChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"


class EOnboardingStep(str, Enum):
    PERSONAL_INFO = "PERSONAL_INFO"
    CONTACT_VERIFICATION = "CONTACT_VERIFICATION"
    SET_PASSWORD = "SET_PASSWORD"
    ADDRESS = "ADDRESS"
    DOCUMENTS = "DOCUMENTS"
    SUBMIT = "SUBMIT"
    COMPLETED = "COMPLETED"


class EOnboardingStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"


class EWaitlistStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INVITED = "INVITED"
    CONVERTED = "CONVERTED"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"


class EVerificationStatus(str, Enum):
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"


class EDocumentSide(str, Enum):
    FRONT = "FRONT"
    BACK = "BACK"
    SINGLE = "SINGLE"
    EXTRA = "EXTRA"


class OnboardingStartDTO(BaseModel):
    email: str
    phone_code: str
    phone_number: str
    invite_token: Optional[str] = None


class OnboardingStartResponseDTO(BaseModel):
    next_step: EOnboardingStep
    invite_token_valid: bool


class PersonalInfoDTO(BaseModel):
    email: str
    phone_code: str
    phone_number: str
    invite_token: Optional[str] = None
    first_name: str
    last_name: str
    second_last_name: Optional[str] = None
    birth_date: date
    key_birth_country: str
    key_birth_state: Optional[str] = None
    type_gender: Optional[str] = None
    key_nationality: Optional[str] = None
    curp: Optional[str] = None


class OtpSendDTO(BaseModel):
    channel: EOtpChannel = EOtpChannel.EMAIL
    destination: str


class OtpVerifyDTO(BaseModel):
    uuid_challenge: str
    code: str
    channel: EOtpChannel = EOtpChannel.EMAIL


class PasswordSetupDTO(BaseModel):
    password: str
    confirm_password: str


class AddressDTO(BaseModel):
    postal_code: str
    key_state: str
    key_municipality: str
    key_colony: Optional[str] = None
    address: str
    address_complement: Optional[str] = None


class DocumentUploadDTO(BaseModel):
    uuid_document_subtype: UUID
    title: Optional[str] = None


class OnboardingResponseDTO(BaseModel):
    uuid_person: str
    current_step: EOnboardingStep
    status: EOnboardingStatus


class OtpSentResponseDTO(BaseModel):
    uuid_challenge: str
    channel: EOtpChannel
    destination: str
    expires_in_minutes: int


class DocumentResponseDTO(BaseModel):
    uuid_document: str
    verification_status: EVerificationStatus


class CheckEmailResponseDTO(BaseModel):
    registered: bool
    status: Optional[EWaitlistStatus] = None


class InviteResponseDTO(BaseModel):
    email: str
    status: EWaitlistStatus
    invite_token: str
    token_expires_at: str


class RegisterLeadDTO(BaseModel):
    client_name: str
    email: str
    source: Optional[str] = None


class LeadResponseDTO(BaseModel):
    id: str
    client_name: str
    email: str
    status: EWaitlistStatus
    source: Optional[str] = None
    created_at: str


class LegacyRegistroBody(BaseModel):
    rol: int
    correo: str
    telefono: str
    code_telefono: str
    contrasena: str


class LegacyCurpBody(BaseModel):
    curp: Optional[str] = None
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    fechaNacimiento: str
    sexo: str
    nacionalidad: Optional[str] = None
    entidadNacimiento: Optional[str] = None


class LegacyDireccionBody(BaseModel):
    codigoPostal: str
    colonia: Optional[str] = None
    estado: str
    municipio: str
    ciudad: Optional[str] = None
    calle: str
    numeroExterior: str
    numeroInterior: Optional[str] = None
    referencia: Optional[str] = None
