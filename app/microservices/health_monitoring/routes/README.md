# Routes

## Overview

Endpoint handlers for Health Monitoring.

## Files

- [people.py](people.py) - People CRUD
- [measurements.py](measurements.py) - Measurements CRUD
- [measure_types.py](measure_types.py) - MeasureTypes CRUD
- [measure_groups.py](measure_groups.py) - MeasureGroups CRUD
- [relations.py](relations.py) - Type-group relations
- [units.py](units.py) - Units CRUD
- [reports.py](reports.py) - Reports endpoints
- [batch.py](batch.py) - Batch operations
- [monitoring_backend.py](monitoring_backend.py) - Backend health/version

## Purpose

HTTP handlers that proxy to Health Monitoring backend via http_client.
