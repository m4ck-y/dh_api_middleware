"""IAM routes."""

from app.microservices.iam.routes import (
    tenants,
    resources,
    operations,
    permissions,
    roles,
    memberships,
    context,
)

__all__ = [
    "tenants",
    "resources",
    "operations",
    "permissions",
    "roles",
    "memberships",
    "context",
]