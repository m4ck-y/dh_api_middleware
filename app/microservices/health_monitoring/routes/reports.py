"""Reports endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.http_client import request
from app.microservices.health_monitoring.app import HEALTH_MONITORING_URL
from app.microservices.health_monitoring.domain import (
    ApiResponsePaginated,
    MeasurementAggregation,
    MeasurementRead,
    MeasureTypeRead,
    MeasureTypeStatsResponse,
)

router = APIRouter(tags=["Reports"])


@router.get(
    "/people/{uuid_person}/measurements",
    response_model=ApiResponsePaginated[MeasurementRead],
)
async def person_measurements(uuid_person: str):
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"people/{uuid_person}/measurements"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/{uuid_type}/stats", response_model=MeasureTypeStatsResponse)
async def measure_type_stats(
    uuid_type: str,
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
):
    params = {}
    if from_date:
        params["from_date"] = from_date
    if to_date:
        params["to_date"] = to_date
    status, data = await request(
        HEALTH_MONITORING_URL,
        "GET",
        f"measure/types/{uuid_type}/stats",
        params=params or None,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{uuid_person}/measurements/latest",
    response_model=ApiResponsePaginated[MeasurementRead],
)
async def person_latest_measurements(uuid_person: str):
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"people/{uuid_person}/measurements/latest"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{uuid_person}/measure/types",
    response_model=ApiResponsePaginated[MeasureTypeRead],
)
async def person_measure_types(uuid_person: str):
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", f"people/{uuid_person}/measure/types"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/measurements/latest-by-person-type",
    response_model=ApiResponsePaginated[MeasurementRead],
)
async def latest_by_person_type():
    status, data = await request(
        HEALTH_MONITORING_URL, "GET", "measurements/latest-by-person-type"
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{uuid_person}/measurements/yearly",
    response_model=list[MeasurementAggregation],
)
async def yearly_measurements(
    uuid_person: str,
    year: int = Query(...),
    uuid_measure_type: Optional[str] = Query(None),
):
    params = {"year": year}
    if uuid_measure_type:
        params["uuid_measure_type"] = uuid_measure_type
    status, data = await request(
        HEALTH_MONITORING_URL,
        "GET",
        f"people/{uuid_person}/measurements/yearly",
        params=params,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{uuid_person}/measurements/monthly",
    response_model=list[MeasurementAggregation],
)
async def monthly_measurements(
    uuid_person: str,
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    uuid_measure_type: Optional[str] = Query(None),
):
    params = {"year": year, "month": month}
    if uuid_measure_type:
        params["uuid_measure_type"] = uuid_measure_type
    status, data = await request(
        HEALTH_MONITORING_URL,
        "GET",
        f"people/{uuid_person}/measurements/monthly",
        params=params,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{uuid_person}/measurements/weekly",
    response_model=list[MeasurementAggregation],
)
async def weekly_measurements(
    uuid_person: str,
    year: int = Query(...),
    week: int = Query(..., ge=1, le=53),
    uuid_measure_type: Optional[str] = Query(None),
):
    params = {"year": year, "week": week}
    if uuid_measure_type:
        params["uuid_measure_type"] = uuid_measure_type
    status, data = await request(
        HEALTH_MONITORING_URL,
        "GET",
        f"people/{uuid_person}/measurements/weekly",
        params=params,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{uuid_person}/measurements/daily",
    response_model=ApiResponsePaginated[MeasurementRead],
)
async def daily_measurements(
    uuid_person: str,
    date: str = Query(..., description="YYYY-MM-DD"),
    uuid_measure_type: Optional[str] = Query(None),
):
    params = {"date": date}
    if uuid_measure_type:
        params["uuid_measure_type"] = uuid_measure_type
    status, data = await request(
        HEALTH_MONITORING_URL,
        "GET",
        f"people/{uuid_person}/measurements/daily",
        params=params,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
