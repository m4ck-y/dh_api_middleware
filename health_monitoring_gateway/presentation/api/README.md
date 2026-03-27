# Presentation API

## Overview

FastAPI application factory and dependency injection.

## Files

- [factory.py](factory.py) - FastAPI app creation and lifespan
- [dependencies.py](dependencies.py) - Dependency injection providers
- [routes/](routes/) - API route definitions

## Purpose

Creates the FastAPI application, manages lifecycle (httpx client), and assembles all routers. Provides dependency injection for backend clients.
