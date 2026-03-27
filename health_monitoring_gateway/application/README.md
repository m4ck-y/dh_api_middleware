# Application Layer

## Overview

Use case orchestration for backend HTTP communication.

## Files

- [call_health_monitoring_backend.py](call_health_monitoring_backend.py) - Orchestrates backend calls

## Purpose

Provides CallHealthMonitoringBackend use case that validates HTTP methods, normalizes paths, and delegates to the backend port without coupling to transport details.

## Exports

- CallHealthMonitoringBackend - Use case for backend HTTP orchestration
- BackendHttpMethodNotAllowedError - Exception for invalid HTTP methods
