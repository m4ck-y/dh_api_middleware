# Gateway Routes

## Overview

Documented proxy routers mirroring Health Monitoring backend endpoints.

## Files

- [batch.py](batch.py) - Batch operations endpoint
- [measure_groups.py](measure_groups.py) - Measure groups endpoint
- [measure_types.py](measure_types.py) - Measure types endpoint
- [measurements.py](measurements.py) - Measurements endpoint
- [monitoring_backend.py](monitoring_backend.py) - Backend health/version endpoint
- [people.py](people.py) - People endpoint
- [relations.py](relations.py) - Relations endpoint (measure type to groups)
- [reports.py](reports.py) - Reports endpoint
- [units.py](units.py) - Units endpoint

## Purpose

Each router exposes a Health Monitoring API endpoint under `/health_monitoring`. Proxies requests to backend with full OpenAPI documentation via Pydantic schemas.

## Exports

- batch.router - Batch operations
- measure_groups.router - Measure groups CRUD
- measure_types.router - Measure types CRUD
- measurements.router - Measurements CRUD
- monitoring_backend.router - Backend health/version
- people.router - People CRUD
- relations.router - Measure type-group relations
- reports.router - Reports generation
- units.router - Units CRUD
