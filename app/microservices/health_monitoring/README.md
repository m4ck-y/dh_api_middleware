# Health Monitoring

## Overview

Health Monitoring microservice proxy.

## Files

- [app.py](app.py) - Sub-app factory + URL constant
- [domain/](domain/) - Pydantic schemas
- [routes/](routes/) - Endpoint handlers

## Purpose

Proxies requests to Health Monitoring backend. Mounted at /health_monitoring.

## Exports

- create_app - Sub-app factory
- HEALTH_MONITORING_URL - Backend URL from env
