"""Batch Operations endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from health_monitoring_gateway.domain.schemas import (
    MeasurementCreate,
    MeasurementRead,
    MessageResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["Batch Operations"])


@router.post("/v2/measurements/batch", response_model=list[MeasurementRead])
async def batch_create_measurements(payload: list[MeasurementCreate]):
    body = [m.model_dump(mode="json") for m in payload]
    status, data = await request("POST", "v2/measurements/batch", json=body)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/v2/measurements/batch-delete", response_model=MessageResponse)
async def batch_delete_measurements(ids: list[int] = Body(..., examples=[[1, 2, 3]])):
    status, data = await request("DELETE", "v2/measurements/batch-delete", json=ids)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
