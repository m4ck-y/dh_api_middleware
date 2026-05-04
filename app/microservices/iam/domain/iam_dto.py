"""IAM domain schemas."""

from enum import Enum
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel, Field


# ── Enums (duplicated from dh_shared) ──────────────────────────────────────────

class ETenantType(str, Enum):
    SYSTEM = "SYSTEM"
    COMPANY = "COMPANY"


class EMembershipStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


# ── Tenant ─────────────────────────────────────────────────────────────────────

class TenantCreateDTO(BaseModel):
    key: str = Field(..., description="Programmatic slug for the tenant (unique).")
    name: str = Field(..., description="Human-readable name of the tenant.")
    type: ETenantType = Field(..., description="Type of tenant — SYSTEM (global) or COMPANY (organization).")
    id_company: Optional[int] = Field(None, description="Logical FK to organizations.company.id (no FK constraint).")
    description: Optional[str] = Field(None, description="Optional description of the tenant.")


class TenantUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, description="Updated tenant name.")
    description: Optional[str] = Field(None, description="Updated description.")


class TenantResponseDTO(BaseModel):
    uuid: UUID = Field(..., description="Tenant UUID.")
    key: str = Field(..., description="Programmatic slug.")
    name: str = Field(..., description="Tenant name.")
    type: ETenantType = Field(..., description="Tenant type.")
    description: Optional[str] = Field(None, description="Tenant description.")


# ── Resource ───────────────────────────────────────────────────────────────────

class ResourceCreateDTO(BaseModel):
    key: str = Field(..., description="Resource key (slug).")
    name: str = Field(..., description="Resource display name.")


class ResourceUpdateDTO(BaseModel):
    name: str = Field(..., description="Updated resource display name.")


class ResourceResponseDTO(BaseModel):
    uuid: UUID = Field(..., description="Resource UUID.")
    key: str = Field(..., description="Resource key.")
    name: str = Field(..., description="Resource display name.")


# ── Operation ──────────────────────────────────────────────────────────────────

class OperationCreateDTO(BaseModel):
    key: str = Field(..., description="Operation key (verb).")
    name: str = Field(..., description="Operation display name.")


class OperationUpdateDTO(BaseModel):
    name: str = Field(..., description="Updated operation display name.")


class OperationResponseDTO(BaseModel):
    uuid: UUID = Field(..., description="Operation UUID.")
    key: str = Field(..., description="Operation key.")
    name: str = Field(..., description="Operation display name.")


# ── Permission ─────────────────────────────────────────────────────────────────

class PermissionCreateDTO(BaseModel):
    uuid_resource: UUID = Field(..., description="UUID of the resource.")
    uuid_operation: UUID = Field(..., description="UUID of the operation.")
    key: Optional[str] = Field(None, description="Permission key (resource:operation). Auto-generated if omitted.")
    description: Optional[str] = Field(None, description="Permission description.")


class PermissionResponseDTO(BaseModel):
    uuid: UUID = Field(..., description="Permission UUID.")
    key: str = Field(..., description="Permission key.")
    description: Optional[str] = Field(None, description="Permission description.")
    is_active: bool = Field(..., description="Whether the permission is active.")


# ── Role ───────────────────────────────────────────────────────────────────────

class RoleCreateDTO(BaseModel):
    uuid_tenant: UUID = Field(..., description="UUID of the tenant.")
    key: str = Field(..., description="Role slug (unique per tenant).")
    name: str = Field(..., description="Role display name.")
    description: Optional[str] = Field(None, description="Role description.")
    uuid_permissions: List[UUID] = Field(default_factory=list, description="List of permission UUIDs to assign to this role.")


class RoleUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, description="Updated role name.")
    description: Optional[str] = Field(None, description="Updated description.")


class RoleResponseDTO(BaseModel):
    uuid: UUID = Field(..., description="Role UUID.")
    key: str = Field(..., description="Role slug.")
    name: str = Field(..., description="Role display name.")
    description: Optional[str] = Field(None, description="Role description.")
    permissions: List[PermissionResponseDTO] = Field(default_factory=list, description="Permissions assigned to this role.")


class RolePermissionsAssignDTO(BaseModel):
    uuid_permissions: List[UUID] = Field(..., description="List of permission UUIDs to assign to the role.")


# ── Membership ─────────────────────────────────────────────────────────────────

class MembershipCreateDTO(BaseModel):
    uuid_person: UUID = Field(..., description="UUID of the person.")
    uuid_tenant: UUID = Field(..., description="UUID of the tenant.")
    uuid_roles: List[UUID] = Field(default_factory=list, description="List of role UUIDs to assign to this membership.")


class MembershipUpdateDTO(BaseModel):
    status: Optional[EMembershipStatus] = Field(None, description="New membership status.")
    uuid_roles: Optional[List[UUID]] = Field(None, description="Replacement role UUIDs.")


class MembershipResponseDTO(BaseModel):
    uuid: UUID = Field(..., description="Membership UUID.")
    status: EMembershipStatus = Field(..., description="Current membership status.")
    roles: List[RoleResponseDTO] = Field(default_factory=list, description="Roles assigned through this membership.")


# ── Context ────────────────────────────────────────────────────────────────────

class ContextResponseDTO(BaseModel):
    """Aggregated IAM context for a person — consumed by dh_auth for JWT injection."""

    roles: List[str] = Field(..., description="Aggregated role keys across all active memberships.")
    permissions: List[str] = Field(..., description="Aggregated permission keys across all assigned roles.")