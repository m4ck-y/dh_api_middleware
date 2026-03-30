# App

## Overview

Main application package containing gateway, services, and configuration.

## Files

- [gateway.py](gateway.py) - Main FastAPI app factory
- [http_client.py](http_client.py) - Shared HTTP client for backend calls
- [main.py](main.py) - Entry point
- [internal/](internal/) - Gateway endpoints (health)
- [settings/](settings/) - Environment configuration
- [microservices/](microservices/) - Microservice sub-apps

## Purpose

Central HTTP proxy gateway. Stateless, no database. Forwards requests to backend services.

## Exports

- create_app - Main gateway factory
- request - HTTP client function
