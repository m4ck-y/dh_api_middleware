# Domain Layer

## Overview

Backend HTTP contracts and Pydantic DTOs aligned with Health Monitoring API.

## Files

- [backend_http.py](backend_http.py) - Backend port and response contracts
- [schemas/](schemas/) - Pydantic schemas mirroring backend models

## Purpose

Defines HealthMonitoringBackendPort protocol and BackendHttpResponse DTO. Contains no I/O logic, only contracts and domain models.

## Exports

- HealthMonitoringBackendPort - Protocol for backend HTTP calls
- BackendHttpResponse - Normalized HTTP response from backend
- HealthMonitoringTransportError - Transport-level exception
