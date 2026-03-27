# Health Monitoring Gateway

## Overview

HTTP gateway/middleware that proxies requests to the Health Monitoring backend, providing a unified entry point with optional cross-cutting concerns.

## Files

- [application/](application/) - Use case orchestration
- [domain/](domain/) - Backend contracts and DTOs
- [infrastructure/](infrastructure/) - HTTP client and settings
- [presentation/](presentation/) - FastAPI routes and handlers

## Purpose

Bounded context for Health Monitoring API gateway. Exposes `/health_monitoring/*` routes that delegate to the backend via HTTP, enabling firewall logic without modifying backend code.

## Exports

- HttpxHealthMonitoringBackend - HTTP client for backend communication
- CallHealthMonitoringBackend - Use case for orchestrating backend calls
- get_settings - Configuration loader
