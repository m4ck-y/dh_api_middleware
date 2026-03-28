# Domain Layer

## Overview

Pydantic schemas for API documentation.

## Files

- [backend_http.py](backend_http.py) - Backend HTTP contracts
- [schemas/](schemas/) - Pydantic DTOs

## Purpose

Contains DTOs aligned with Health Monitoring backend for OpenAPI documentation.

## Exports

- PersonCreate, PersonRead, PersonUpdate
- MeasurementCreate, MeasurementRead
- MeasureTypeCreate, MeasureTypeRead
- MeasureGroupCreate, MeasureGroupRead
- MeasureTypeGroupCreate, MeasureTypeGroupRead, MeasureTypeGroupRelation
- UnitCreate, UnitRead
- MeasurementAggregation
- CountResponse, MessageResponse, BackendHealthStatusResponse, BackendVersionResponse
