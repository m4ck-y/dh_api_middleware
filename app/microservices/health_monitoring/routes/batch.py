"""Batch Operations endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    MeasurementCreate,
    MeasurementRead,
    MessageResponse,
)

router = APIRouter(tags=["Batch Operations"])


@router.post("/v2/measurements/batch", response_model=list[MeasurementRead])
async def batch_create_measurements(payload: list[MeasurementCreate]):
    body = [m.model_dump(mode="json") for m in payload]
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "v2/measurements/batch", json=body
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/v2/measurements/batch-delete", response_model=MessageResponse)
async def batch_delete_measurements(ids: list[int] = Body(..., examples=[[1, 2, 3]])):
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", "v2/measurements/batch-delete", json=ids
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
