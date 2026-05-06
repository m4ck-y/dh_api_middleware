from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


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


class EIdentifierType(str, Enum):
    CURP = "CURP"
    RFC = "RFC"
    NSS = "NSS"
    PASSPORT = "PASSPORT"
    NATIONAL_ID = "NATIONAL_ID"
    OTHER = "OTHER"


class OnboardingStartDTO(BaseModel):
    email: EmailStr = Field(..., description="Email del applicant.", examples=["juan@example.com"])
    phone_code: str = Field(..., description="Código de país/lada.", examples=["+52"])
    phone_number: str = Field(..., description="Número de teléfono sin lada.", examples=["5512345678"])
    invite_token: Optional[str] = Field(None, description="Token de invitación de la waitlist. Enviar null u omitir para registro abierto sin waitlist.", examples=[None, "tok_abc123"])

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class PersonalIdentifierInputDTO(BaseModel):
    type: EIdentifierType = Field(default=EIdentifierType.NATIONAL_ID, description="Tipo de identificador.", examples=["NATIONAL_ID"])
    value: str = Field(..., description="Valor del identificador (CURP, NSS, RFC).", examples=["PEGJ900515HJCRRC09"])


class OnboardingStartResponseDTO(BaseModel):
    next_step: EOnboardingStep = Field(EOnboardingStep.PERSONAL_INFO, description="Siguiente paso del flujo.")
    invite_token_valid: bool = Field(..., description="Si se proporcionó token, indica si es válido y no ha expirado.")


class PersonalInfoDTO(BaseModel):
    email: EmailStr = Field(..., description="Email del applicant.", examples=["juan@example.com"])
    phone_code: str = Field(..., description="Código de país/lada.", examples=["+52"])
    phone_number: str = Field(..., description="Número de teléfono sin lada.", examples=["5512345678"])
    invite_token: Optional[str] = Field(None, description="Token de invitación original (re-validado al crear la Person).")
    first_name: str = Field(..., description="Nombre(s).", examples=["Juan"])
    last_name: str = Field(..., description="Apellido paterno.", examples=["Pérez"])
    second_last_name: Optional[str] = Field(None, description="Apellido materno.", examples=["García"])
    birth_date: date = Field(..., description="Fecha de nacimiento.", examples=["1990-05-15"])
    key_birth_country: str = Field(..., description="Clave de país de nacimiento (catálogo).", examples=["MEX"])
    key_birth_state: Optional[str] = Field(None, description="Clave de entidad federativa de nacimiento (catálogo).", examples=["JAL"])
    type_gender: Optional[str] = Field(None, description="Identidad de género (EGenderIdentity).", examples=["MASCULINO"])
    key_nationality: Optional[str] = Field(None, description="Clave de nacionalidad (catálogo).", examples=["MEX"])
    personal_identifier: Optional[PersonalIdentifierInputDTO] = Field(None, description="Identificador personal opcional (CURP, NSS, RFC).")

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class OtpSendDTO(BaseModel):
    channel: EOtpChannel = Field(EOtpChannel.EMAIL, description="Canal de envío del OTP.", examples=["EMAIL"])
    destination: str = Field(..., description="Email o teléfono al que enviar el código.", examples=["juan@example.com"])


class OtpVerifyDTO(BaseModel):
    uuid_challenge: str = Field(..., description="ID del challenge devuelto por /otp/send.", examples=["64f1a2b3c4d5e6f7a8b9c0d1"])
    code: str = Field(..., description="Código OTP recibido.", examples=["123456"])
    channel: EOtpChannel = Field(EOtpChannel.EMAIL, description="Canal por el que se recibió.", examples=["EMAIL"])


class PasswordSetupDTO(BaseModel):
    password: str = Field(..., min_length=8, description="Contraseña.", examples=["MySecurePass123!"])
    confirm_password: str = Field(..., description="Confirmación de contraseña.", examples=["MySecurePass123!"])


class AddressDTO(BaseModel):
    postal_code: str = Field(..., description="Código postal.", examples=["44100"])
    key_state: str = Field(..., description="Clave de estado (catálogo).", examples=["JAL"])
    key_municipality: str = Field(..., description="Clave de municipio (catálogo).", examples=["039"])
    key_colony: Optional[str] = Field(None, description="Clave de colonia (catálogo).", examples=["1234"])
    address: str = Field(..., description="Calle y número exterior.", examples=["Av. Juárez 45"])
    address_complement: Optional[str] = Field(None, description="Número interior y referencia.", examples=["Int. 3, frente al parque"])


class DocumentFileDTO(BaseModel):
    side: EDocumentSide = Field(..., description="Lado o variante del archivo (FRONT, BACK, SINGLE, EXTRA).", examples=["FRONT"])
    url: str = Field(..., description="URL del archivo en storage.")
    url_thumbnail: Optional[str] = Field(None, description="URL del thumbnail generado. Null si no aplica.")
    mime_type: Optional[str] = Field(None, description="MIME type del archivo.", examples=["image/jpeg"])
    size_bytes: Optional[int] = Field(None, description="Tamaño del archivo en bytes.", examples=[245678])


class DocumentUploadDTO(BaseModel):
    uuid_document_subtype: UUID = Field(..., description="UUID del subtipo de documento según catálogo expedient.document_subtype.", examples=["550e8400-e29b-41d4-a716-446655440000"])
    title: Optional[str] = Field(None, description="Título del documento.", examples=["INE de Juan"])


class OnboardingResponseDTO(BaseModel):
    uuid_person: str = Field(..., description="UUID de la Person en PostgreSQL.", examples=["550e8400-e29b-41d4-a716-446655440000"])
    current_step: EOnboardingStep = Field(..., description="Siguiente paso del flujo.")
    status: EOnboardingStatus = Field(..., description="Estado del proceso.")


class OtpSentResponseDTO(BaseModel):
    uuid_challenge: str = Field(..., description="ID del challenge en dh_mfa. Necesario para llamar a /otp/verify.", examples=["64f1a2b3c4d5e6f7a8b9c0d1"])
    channel: EOtpChannel = Field(..., description="Canal por el que se envió el código.")
    destination: str = Field(..., description="Destino enmascarado.", examples=["j***@example.com"])
    expires_in_minutes: int = Field(..., description="Minutos de validez.", examples=[10])


class DocumentResponseDTO(BaseModel):
    uuid_document: str = Field(..., description="UUID del documento creado.")
    verification_status: EVerificationStatus = Field(..., description="Estado de verificación del documento.", examples=["PENDING"])


class CheckEmailResponseDTO(BaseModel):
    registered: bool = Field(
        ...,
        description="Whether the email is already in the waitlist.",
        examples=[True],
    )
    status: Optional[EWaitlistStatus] = Field(
        None,
        description="Current lifecycle status of the lead, if registered.",
        examples=["ACTIVE"],
    )


class InviteResponseDTO(BaseModel):
    email: str = Field(..., description="Email of the invited lead.", examples=["juan.perez@example.com"])
    status: EWaitlistStatus = Field(..., description="Updated lead status.", examples=["INVITED"])
    invite_token: str = Field(..., description="Secure token to start onboarding. Send this to the lead.", examples=["tok_a1b2c3d4"])
    token_expires_at: datetime = Field(..., description="UTC expiry of the invite token.", examples=["2026-05-03T10:30:00Z"])


class RegisterLeadDTO(BaseModel):
    client_name: str = Field(
        ...,
        description="Name of the lead. Can be a person or a company.",
        examples=["Juan Pérez", "Clínica San Rafael"],
    )
    email: EmailStr = Field(
        ...,
        description="Email address of the lead. Must be unique in the waitlist.",
        examples=["juan.perez@example.com"],
    )
    source: Optional[str] = Field(
        None,
        description="Origin channel of the lead.",
        examples=["landing_page", "referral", "ads", "partner", "waitlist_form"],
    )

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class LeadResponseDTO(BaseModel):
    id: str = Field(
        ...,
        description="Unique MongoDB identifier of the waitlist record.",
        examples=["64f1a2b3c4d5e6f7a8b9c0d1"],
    )
    client_name: str = Field(
        ...,
        description="Name of the lead.",
        examples=["Juan Pérez"],
    )
    email: str = Field(
        ...,
        description="Email address of the lead.",
        examples=["juan.perez@example.com"],
    )
    status: EWaitlistStatus = Field(
        ...,
        description="Current lifecycle status of the lead.",
        examples=["ACTIVE"],
    )
    source: Optional[str] = Field(
        None,
        description="Origin channel of the lead.",
        examples=["landing_page"],
    )
    created_at: datetime = Field(
        ...,
        description="UTC timestamp of when the lead registered.",
        examples=["2026-04-26T10:30:00Z"],
    )


class LegacyRegistroBody(BaseModel):
    rol: int = Field(..., description="ID del rol a asignar.")
    correo: EmailStr = Field(..., description="Correo electrónico del usuario.", examples=["juan@example.com"])
    telefono: str = Field(..., description="Número de teléfono sin lada.", examples=["5512345678"])
    code_telefono: str = Field(..., description="Código de país/lada.", examples=["+52"])
    contrasena: str = Field(..., min_length=8, description="Contraseña del usuario.", examples=["MySecurePass123!"])

    @field_validator("correo", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class LegacyCurpBody(BaseModel):
    curp: Optional[str] = Field(None, description="CURP (18 caracteres). Opcional.", examples=["PEGJ900515HJCRRC09"])
    nombre: str = Field(..., description="Nombre(s).", examples=["Juan"])
    apellidoPaterno: str = Field(..., description="Apellido paterno.", examples=["Pérez"])
    apellidoMaterno: Optional[str] = Field(None, description="Apellido materno.", examples=["García"])
    fechaNacimiento: str = Field(..., description="Fecha de nacimiento.", examples=["1990-05-15"])
    sexo: str = Field(..., description="Sexo (H/M).", examples=["H"])
    nacionalidad: Optional[str] = Field(None, description="Nacionalidad.", examples=["MEX"])
    entidadNacimiento: Optional[str] = Field(None, description="Entidad federativa de nacimiento.", examples=["JAL"])


class LegacyDireccionBody(BaseModel):
    codigoPostal: str = Field(..., description="Código postal.", examples=["44100"])
    colonia: Optional[str] = Field(None, description="Colonia.", examples=["Centro"])
    estado: str = Field(..., description="Estado.", examples=["JAL"])
    municipio: str = Field(..., description="Municipio.", examples=["Guadalajara"])
    ciudad: Optional[str] = Field(None, description="Ciudad.", examples=["Guadalajara"])
    calle: str = Field(..., description="Calle.", examples=["Av. Juárez"])
    numeroExterior: str = Field(..., description="Número exterior.", examples=["45"])
    numeroInterior: Optional[str] = Field(None, description="Número interior.", examples=["3"])
    referencia: Optional[str] = Field(None, description="Referencia.", examples=["Frente al parque"])
