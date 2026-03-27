from __future__ import annotations

import json
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request

from health_monitoring_gateway.application.call_health_monitoring_backend import (
    CallHealthMonitoringBackend,
)
from health_monitoring_gateway.domain import schemas
from health_monitoring_gateway.presentation.api.dependencies import get_health_monitoring_backend
from health_monitoring_gateway.presentation.backend_http_bridge import (
    backend_json,
    raise_backend_http_error,
)

router = APIRouter(tags=["Batch Operations"])


@router.post(
    "/v2/measurements/batch",
    response_model=list[schemas.MeasurementRead],
)
async def batch_create_measurements(
    request: Request,
    payload: list[schemas.MeasurementCreate],
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
):
    # JSON array body expected by Health Monitoring batch endpoint
    body = json.dumps(
        [m.model_dump(mode="json") for m in payload],
        default=str,
    ).encode()
    status, data = await backend_json(
        request,
        backend,
        "v2/measurements/batch",
        body=body,
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data


@router.delete(
    "/v2/measurements/batch-delete",
    response_model=schemas.MessageResponse,
)
async def batch_delete_measurements(
    request: Request,
    backend: Annotated[CallHealthMonitoringBackend, Depends(get_health_monitoring_backend)],
    ids: list[int] = Body(..., examples=[[1, 2, 3]]),
):
    body = json.dumps(ids).encode()
    status, data = await backend_json(
        request,
        backend,
        "v2/measurements/batch-delete",
        body=body,
        json_request=True,
    )
    raise_backend_http_error(status, data)
    return data
