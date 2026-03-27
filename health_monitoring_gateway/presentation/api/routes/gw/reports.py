from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Request

from health_monitoring_gateway.application.call_health_monitoring_backend import (
    CallHealthMonitoringBackend,
)
from health_monitoring_gateway.domain import schemas
from health_monitoring_gateway.presentation.api.dependencies import get_health_monitoring_backend
from health_monitoring_gateway.presentation.backend_http_bridge import (
    backend_json,
    raise_backend_http_error,
)

router = APIRouter(tags=["Reports"])


@router.get(
    "/people/{person_id}/measurements",
    response_model=list[schemas.MeasurementRead],
)
async def person_measurements(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measurements",
    )
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/measure/types/{id}/stats",
    response_model=schemas.MeasureTypeStatsResponse,
)
async def measure_type_stats(
    request: Request,
    id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
):
    status, data = await backend_json(request, backend, f"measure/types/{id}/stats")
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/people/{person_id}/measurements/latest",
    response_model=list[schemas.MeasurementRead],
)
async def person_latest_measurements(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measurements/latest",
    )
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/people/{person_id}/measure/types",
    response_model=list[schemas.MeasureTypeRead],
)
async def person_measure_types(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measure/types",
    )
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/measurements/latest-by-person-type",
    response_model=list[schemas.MeasurementRead],
)
async def latest_by_person_type(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    status, data = await backend_json(request, backend, "measurements/latest-by-person-type")
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/people/{person_id}/measurements/yearly",
    response_model=list[schemas.MeasurementAggregation],
)
async def yearly_measurements(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    year: int = Query(..., description="Year to query"),
    measure_type_id: Optional[int] = Query(None),
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measurements/yearly",
    )
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/people/{person_id}/measurements/monthly",
    response_model=list[schemas.MeasurementAggregation],
)
async def monthly_measurements(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    measure_type_id: Optional[int] = Query(None),
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measurements/monthly",
    )
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/people/{person_id}/measurements/weekly",
    response_model=list[schemas.MeasurementAggregation],
)
async def weekly_measurements(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    year: int = Query(...),
    week: int = Query(..., ge=1, le=53),
    measure_type_id: Optional[int] = Query(None),
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measurements/weekly",
    )
    raise_backend_http_error(status, data)
    return data


@router.get(
    "/people/{person_id}/measurements/daily",
    response_model=list[schemas.MeasurementRead],
)
async def daily_measurements(
    request: Request,
    person_id: int,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    date: str = Query(..., description="YYYY-MM-DD"),
    measure_type_id: Optional[int] = Query(None),
):
    status, data = await backend_json(
        request,
        backend,
        f"people/{person_id}/measurements/daily",
    )
    raise_backend_http_error(status, data)
    return data
