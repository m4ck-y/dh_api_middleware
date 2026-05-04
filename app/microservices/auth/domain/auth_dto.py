"""Authentication DTOs for the auth microservice."""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class LoginRequestDTO(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User email address.",
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        description="User password in plain text.",
        examples=["MySecurePass123!"],
    )


class LoginResponseDTO(BaseModel):
    message: str = Field(
        ...,
        description="Result message of the login operation.",
        examples=["Login successful"],
    )
    needs_otp: bool = Field(
        ...,
        description="Whether OTP verification is required.",
        examples=[False],
    )
    redirect: str = Field(
        ...,
        description="Redirect URL after login.",
        examples=["/dashboard"],
    )


class MeResponseDTO(BaseModel):
    uuid: UUID = Field(
        ...,
        description="User unique identifier.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    email: str = Field(
        ...,
        description="User email address.",
        examples=["user@example.com"],
    )
    first_name: str | None = Field(
        None,
        description="Given name of the user.",
        examples=["Juan"],
    )
    last_name: str | None = Field(
        None,
        description="Family name of the user.",
        examples=["Perez"],
    )
    is_active: bool = Field(
        ...,
        description="Whether the user account is active.",
        examples=[True],
    )


class MessageResponseDTO(BaseModel):
    message: str = Field(
        ...,
        description="Response message.",
        examples=["Session closed"],
    )
