# Domain Schemas

## Overview

Pydantic DTOs aligned with Health Monitoring backend API for OpenAPI parity.

## Files

- [aggregations.py](aggregations.py) - Measurement aggregation models
- [common.py](common.py) - Shared response models
- [measure_groups.py](measure_groups.py) - MeasureGroup create/read models
- [measure_type_groups.py](measure_type_groups.py) - MeasureTypeGroup models
- [measure_types.py](measure_types.py) - MeasureType create/read models
- [measurements.py](measurements.py) - Measurement create/read models
- [person.py](person.py) - Person create/read/update models
- [units.py](units.py) - Unit create/read models

## Purpose

Mirrors Health Monitoring backend schemas to ensure Swagger documentation matches the backend contract. Must be updated when backend schemas change.

## Exports

- PersonCreate, PersonRead, PersonUpdate - Person DTOs
- MeasurementCreate, MeasurementRead - Measurement DTOs
- MeasureTypeCreate, MeasureTypeRead - MeasureType DTOs
- MeasureGroupCreate, MeasureGroupRead - MeasureGroup DTOs
- MeasureTypeGroupCreate, MeasureTypeGroupRead, MeasureTypeGroupRelation - MeasureTypeGroup DTOs
- UnitCreate, UnitRead - Unit DTOs
- MeasurementAggregation, MeasurementAggregationList - Aggregation DTOs
- CountResponse, JsonObjectResponse, MessageResponse, BackendHealthStatusResponse, BackendVersionResponse - Common responses
