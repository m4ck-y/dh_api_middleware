# Health Monitoring Gateway

## Overview

Gateway service for Health Monitoring microservice. Proxies requests to backend via HTTP.

## Files

- [domain/](domain/) - Pydantic schemas
- [infrastructure/](infrastructure/) - HTTP client
- [presentation/](presentation/) - FastAPI routes

## Purpose

Provides `/health_monitoring/*` routes that proxy to Health Monitoring backend. Stateless HTTP proxy with no database access. Security layer: if compromised, attacker only accesses this proxy, not actual services.

## Exports

- create_health_monitoring_app - Sub-app factory with own /docs
