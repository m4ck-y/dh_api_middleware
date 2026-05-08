"""IAM API - Identity and Access Management.

## Test UI

Preview: [{service_url}]({service_url})

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

Proxies to: [{service_url}/docs]({service_url}/docs)
"""

from __future__ import annotations

from fastapi import FastAPI

from app.settings import settings

IAM_URL = settings.SERVICE_IAM_URL.rstrip("/")
_DESC = __doc__.replace("{service_url}", IAM_URL) if IAM_URL else __doc__


def create_app(root_path: str = "") -> FastAPI:
    app = FastAPI(
        title="IAM API",
        version="0.1.0",
        description=_DESC,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path=root_path,
    )

    from app.microservices.iam.routes.v1 import (
        tenants,
        resources,
        operations,
        permissions,
        roles,
        memberships,
        context,
    )

    for m in [tenants, resources, operations, permissions, roles, memberships, context]:
        app.include_router(m.router)

    return app