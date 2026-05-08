"""API Gateway - Central HTTP proxy for microservices.

## Overview

Stateless gateway that proxies requests to backend services.
Frontend points here instead of individual microservices.

## Security

- **NO database**: Pure HTTP proxy
- If compromised, attacker only accesses this proxy

## Services

| Service | Status | Docs | Prefix |
|---------|--------|------|--------|
| Main | RELEASED | [{root_path}/docs]({root_path}/docs) | `/` |
| Auth | RELEASED | [{root_path}/auth/docs]({root_path}/auth/docs) | `/auth` |
| IAM | RELEASED | [{root_path}/iam/docs]({root_path}/iam/docs) | `/iam` |
| Core | RELEASED | [{root_path}/core/docs]({root_path}/core/docs) | `/core` |
| MFA | RELEASED | [{root_path}/mfa/docs]({root_path}/mfa/docs) | `/mfa` |
| Onboarding | RELEASED | [{root_path}/onboarding/docs]({root_path}/onboarding/docs) | `/onboarding` |
| Storage | RELEASED | [{root_path}/storage/docs]({root_path}/storage/docs) | `/storage` |
| Health Monitoring | RELEASED | [{root_path}/health_monitoring/docs]({root_path}/health_monitoring/docs) | `/health_monitoring` |
| Message Sender | TESTING | [{root_path}/message_sender/docs]({root_path}/message_sender/docs) | `/message_sender` |
| Logger Tracer | TESTING | [{root_path}/logger_tracer/docs]({root_path}/logger_tracer/docs) | `/logger_tracer` |
| Admin | RELEASED | [{root_path}/admin/docs]({root_path}/admin/docs) | `/admin` |
| Catalogs | PENDING | — | `/catalogs` |
| Organizations | PENDING | — | `/organizations` |

## Environment

Configure services with `SERVICE_<NAME>_URL` environment variables.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings


def create_app() -> FastAPI:
    """Create main gateway application."""
    root_path = settings.ROOT_PATH.rstrip("/")
    app = FastAPI(
        root_path=settings.ROOT_PATH,
        title="API Gateway",
        version="0.1.0",
        description=__doc__.format(root_path=root_path),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.internal.health import router as health_router
    app.include_router(health_router)

    # ── RELEASED ─────────────────────────────────────────────────
    from app.microservices.auth.app import create_app as create_auth
    from app.microservices.iam.app import create_app as create_iam
    from app.microservices.core.app import create_app as create_core
    from app.microservices.mfa.app import create_app as create_mfa
    from app.microservices.onboarding.app import create_app as create_onboarding
    from app.microservices.health_monitoring.app import create_app as create_health_monitoring

    app.mount("/auth", create_auth(root_path=f"{root_path}/auth"))
    app.mount("/iam", create_iam(root_path=f"{root_path}/iam"))
    app.mount("/core", create_core(root_path=f"{root_path}/core"))
    app.mount("/mfa", create_mfa(root_path=f"{root_path}/mfa"))
    app.mount("/onboarding", create_onboarding(root_path=f"{root_path}/onboarding"))
    app.mount("/health_monitoring", create_health_monitoring(root_path=f"{root_path}/health_monitoring"))

    # ── TESTING ──────────────────────────────────────────────────
    from app.microservices.message_sender.app import create_app as create_message_sender
    from app.microservices.logger_tracer.app import create_app as create_logger_tracer

    app.mount("/message_sender", create_message_sender(root_path=f"{root_path}/message_sender"))
    app.mount("/logger_tracer", create_logger_tracer(root_path=f"{root_path}/logger_tracer"))

    # ── PENDING: catalogs, organizations, expedient ──────────────

    return app