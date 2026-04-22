from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.http_client import request
from app.settings import settings
from app.shared.domain.api_response import ApiResponsePaginated
from app.microservices.logger_tracer.domain.models import MetricEntry

LOGGER_TRACER_URL = settings.SERVICE_LOGGER_TRACER_URL.rstrip("/")

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/", response_model=ApiResponsePaginated[MetricEntry])
async def get_metrics(
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    page: int = Query(1, ge=1, description="Page number"),
    query: Optional[str] = Query(None, description="MongoDB style filter JSON")
):
    """Retrieve historical metrics."""
    params = {"limit": limit, "page": page}
    if query:
        params["query"] = query
        
    status_code, data = await request(
        LOGGER_TRACER_URL, "GET", "metrics", params=params
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/", status_code=201)
async def create_metric(payload: MetricEntry):
    """Ingest a single metric entry."""
    status_code, data = await request(
        LOGGER_TRACER_URL, "POST", "metrics", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
