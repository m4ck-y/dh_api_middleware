"""IAM API - Identity and Access Management.

## Overview

RBAC with tenants, resources, operations, permissions, roles, and memberships.

## Endpoints

- Tenants CRUD
- Resources CRUD
- Operations CRUD  
- Permissions CRUD
- Roles CRUD
- Memberships CRUD
- GET /context/{uuid_person}

## Backend

Proxies to: `{settings.SERVICE_IAM_URL}`
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

IAM_URL = settings.SERVICE_IAM_URL.rstrip("/")


def create_app() -> FastAPI:
    app = FastAPI(
        title="IAM API",
        version="0.1.0",
        description=__doc__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from app.microservices.iam.routes import (
        tenants,
        resources,
        operations,
        permissions,
        roles,
        memberships,
        context,
    )

    tenants.router.prefix = "/v1/iam/tenants"
    resources.router.prefix = "/v1/iam/resources"
    operations.router.prefix = "/v1/iam/operations"
    permissions.router.prefix = "/v1/iam/permissions"
    roles.router.prefix = "/v1/iam/roles"
    memberships.router.prefix = "/v1/iam/memberships"
    context.router.prefix = "/v1/iam"

    for m in [tenants, resources, operations, permissions, roles, memberships, context]:
        app.include_router(m.router)

    return app