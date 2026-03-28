"""Measure Types endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    CountResponse,
    MeasureTypeCreate,
    MeasureTypeRead,
    MessageResponse,
)

router = APIRouter(tags=["Measure Types"])


@router.get("/measure/types", response_model=list[MeasureTypeRead])
async def list_measure_types():
    status, data = await request(HEALTH_MONITORING_URL, "GET", "measure/types")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/count", response_model=CountResponse)
async def measure_types_count():
    status, data = await request(HEALTH_MONITORING_URL, "GET", "measure/types/count")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/with-data", response_model=list[MeasureTypeRead])
async def measure_types_with_data():
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", "measure/types/with-data"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/{type_id}", response_model=MeasureTypeRead)
async def get_measure_type(type_id: int):
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"measure/types/{type_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/measure/types", response_model=MeasureTypeRead, status_code=201)
async def create_measure_type(payload: MeasureTypeCreate):
    status, data = await request(
        HEALTH_MONITORING_URL, "POST", "measure/types", json=payload.model_dump()
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/measure/types/{type_id}", response_model=MeasureTypeRead)
async def update_measure_type(type_id: int, payload: MeasureTypeCreate):
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PUT",
        f"measure/types/{type_id}",
        json=payload.model_dump(),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/measure/types/{type_id}", response_model=MeasureTypeRead)
async def patch_measure_type(type_id: int, payload: MeasureTypeCreate):
    status, data = await request(
        HEALTH_MONITORING_URL,
        "PATCH",
        f"measure/types/{type_id}",
        json=payload.model_dump(exclude_unset=True),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/measure/types/{type_id}", response_model=MessageResponse)
async def delete_measure_type(type_id: int):
    status, data = await request(
        HEALTH_MONITORING_URL, "DELETE", f"measure/types/{type_id}"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
