"""Authentication DTOs for the auth microservice."""

from pydantic import BaseModel, Field
from uuid import UUID


class CompanyResponseDTO(BaseModel):
    """Company linked to the user's employee record."""

    uuid: UUID = Field(
        ...,
        description="Unique identifier of the company.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    name: str = Field(
        ...,
        description="Registered business name of the company.",
        examples=["Hospital San Rafael S.A.P.I. de C.V."],
    )
    key: str = Field(
        ...,
        description="Programmatic key used to identify the company in API calls.",
        examples=["hospital_san_rafael"],
    )


class EmployeeResponseDTO(BaseModel):
    """Employee record associated with the authenticated person."""

    uuid: UUID = Field(
        ...,
        description="Unique identifier of the employee record.",
        examples=["660e8400-e29b-41d4-a716-446655440001"],
    )
    uuid_person: UUID = Field(
        ...,
        description="Unique identifier of the person linked to this employee record.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    position: str | None = Field(
        None,
        description="Job position or title within the company.",
        examples=["Médico General"],
    )
    company: CompanyResponseDTO | None = Field(
        None,
        description="Company to which this employee belongs.",
    )


class TenantResponseDTO(BaseModel):
    """Tenant (organization) the user has a membership in."""

    uuid: UUID = Field(
        ...,
        description="Unique identifier of the tenant.",
        examples=["770e8400-e29b-41d4-a716-446655440002"],
    )
    key: str = Field(
        ...,
        description="Programmatic key used to identify the tenant in API calls.",
        examples=["clinica_central"],
    )
    name: str = Field(
        ...,
        description="Human-readable name of the tenant.",
        examples=["Clínica Central"],
    )


class LoginRequestDTO(BaseModel):
    """Credentials for user login."""

    username: str = Field(
        ...,
        description="User identifier — email, phone number, or username.",
        examples=["juan@example.com"],
    )
    password: str = Field(
        ...,
        description="User's secret password in plain text. It is hashed server-side with bcrypt.",
        examples=["MySecurePass123!"],
    )


class UserInfoDTO(BaseModel):
    """Minimal user information returned on login."""

    uuid: UUID = Field(
        ...,
        description="User unique identifier.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    username: str = Field(
        ...,
        description="Username used for authentication (email in most cases).",
        examples=["juan.perez@example.com"],
    )
    first_name: str | None = Field(
        None,
        description="Given name(s) of the person.",
        examples=["Juan"],
    )
    last_name: str | None = Field(
        None,
        description="Family name(s) of the person.",
        examples=["Pérez"],
    )
    is_active: bool = Field(
        ...,
        description="Whether the user account is active.",
        examples=[True],
    )
    verification_status: str = Field(
        ...,
        description="Identity verification status of the person.",
        examples=["APPROVED"],
    )


class LoginResponseDTO(BaseModel):
    """Successful login response with user summary."""

    message: str = Field(
        ...,
        description="Result message of the login operation.",
        examples=["Login successful"],
    )
    user: UserInfoDTO = Field(
        ...,
        description="Basic user information returned after authentication.",
    )


class MeResponseDTO(BaseModel):
    """Complete profile of the authenticated user returned by GET /auth/me."""

    uuid: UUID = Field(
        ...,
        description="Person UUID — primary identifier across the system.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    username: str = Field(
        ...,
        description="Username used for authentication (email in most cases).",
        examples=["juan.perez@example.com"],
    )
    first_name: str | None = Field(
        None,
        description="Given name(s) of the person.",
        examples=["Juan"],
    )
    last_name: str | None = Field(
        None,
        description="Family name(s) of the person.",
        examples=["Pérez"],
    )
    verification_status: str = Field(
        ...,
        description="Identity verification status of the person.",
        examples=["APPROVED"],
    )
    employee: EmployeeResponseDTO | None = Field(
        None,
        description="Employee record if the person is linked to a company.",
    )
    tenants: list[TenantResponseDTO] = Field(
        default_factory=list,
        description="List of tenants (organizations) the user has access to.",
    )
    roles: list[str] = Field(
        default_factory=list,
        description="Assigned role names within the active tenant context.",
        examples=[["ADMIN", "DOCTOR"]],
    )
    permissions: list[str] = Field(
        default_factory=list,
        description="Granular permissions granted through the assigned roles (recurso:operacion).",
        examples=[["user:create", "patient:view"]],
    )


class MessageResponseDTO(BaseModel):
    message: str = Field(
        ...,
        description="Response message.",
        examples=["Token refreshed"],
    )
