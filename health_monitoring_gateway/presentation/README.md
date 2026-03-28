# Presentation Layer

## Overview

FastAPI HTTP handlers and route definitions.

## Files

- [api/](api/) - FastAPI app factory and routes

## Purpose

Contains HTTP presentation logic: FastAPI routers and request handlers. Each route proxies to Health Monitoring backend via httpx.

## Exports

- create_app - Main gateway app factory
- create_health_monitoring_app - Health Monitoring sub-app factory
