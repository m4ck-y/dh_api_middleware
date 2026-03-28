"""Reports endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from health_monitoring_gateway.domain.schemas import (
    MeasurementRead,
    MeasureTypeRead,
    MeasurementAggregation,
    MeasureTypeStatsResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["Reports"])


@router.get("/people/{person_id}/measurements", response_model=list[MeasurementRead])
async def person_measurements(person_id: int):
    status, data = await request("GET", f"people/{person_id}/measurements")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measure/types/{type_id}/stats", response_model=MeasureTypeStatsResponse)
async def measure_type_stats(
    type_id: int,
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
):
    params = {}
    if from_date:
        params["from_date"] = from_date
    if to_date:
        params["to_date"] = to_date
    status, data = await request(
        "GET", f"measure/types/{type_id}/stats", params=params or None
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{person_id}/measurements/latest", response_model=list[MeasurementRead]
)
async def person_latest_measurements(person_id: int):
    status, data = await request("GET", f"people/{person_id}/measurements/latest")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/people/{person_id}/measure/types", response_model=list[MeasureTypeRead])
async def person_measure_types(person_id: int):
    status, data = await request("GET", f"people/{person_id}/measure/types")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/measurements/latest-by-person-type", response_model=list[MeasurementRead])
async def latest_by_person_type():
    status, data = await request("GET", "measurements/latest-by-person-type")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{person_id}/measurements/yearly",
    response_model=list[MeasurementAggregation],
)
async def yearly_measurements(
    person_id: int,
    year: int = Query(...),
    measure_type_id: Optional[int] = Query(None),
):
    params = {"year": year}
    if measure_type_id:
        params["measure_type_id"] = measure_type_id
    status, data = await request(
        "GET", f"people/{person_id}/measurements/yearly", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{person_id}/measurements/monthly",
    response_model=list[MeasurementAggregation],
)
async def monthly_measurements(
    person_id: int,
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    measure_type_id: Optional[int] = Query(None),
):
    params = {"year": year, "month": month}
    if measure_type_id:
        params["measure_type_id"] = measure_type_id
    status, data = await request(
        "GET", f"people/{person_id}/measurements/monthly", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{person_id}/measurements/weekly",
    response_model=list[MeasurementAggregation],
)
async def weekly_measurements(
    person_id: int,
    year: int = Query(...),
    week: int = Query(..., ge=1, le=53),
    measure_type_id: Optional[int] = Query(None),
):
    params = {"year": year, "week": week}
    if measure_type_id:
        params["measure_type_id"] = measure_type_id
    status, data = await request(
        "GET", f"people/{person_id}/measurements/weekly", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get(
    "/people/{person_id}/measurements/daily", response_model=list[MeasurementRead]
)
async def daily_measurements(
    person_id: int,
    date: str = Query(..., description="YYYY-MM-DD"),
    measure_type_id: Optional[int] = Query(None),
):
    params = {"date": date}
    if measure_type_id:
        params["measure_type_id"] = measure_type_id
    status, data = await request(
        "GET", f"people/{person_id}/measurements/daily", params=params
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
