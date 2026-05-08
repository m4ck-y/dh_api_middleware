from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.http_client import request
from app.settings import settings
from app.shared.domain.api_response import ApiResponsePaginated, ApiResponseSingle
from app.microservices.logger_tracer.domain.models import TraceEntry

LOGGER_TRACER_URL = settings.SERVICE_LOGGER_TRACER_URL.rstrip("/")

router = APIRouter(prefix="/traces", tags=["Traces"])

@router.get("/", response_model=ApiResponsePaginated[TraceEntry])
async def get_traces(
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    page: int = Query(1, ge=1, description="Page number"),
    query: Optional[str] = Query(None, description="MongoDB style filter JSON")
):
    """Retrieve historical traces."""
    params = {"limit": limit, "page": page}
    if query:
        params["query"] = query
        
    status_code, data = await request(
        LOGGER_TRACER_URL, "GET", "traces", params=params
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/", response_model=ApiResponseSingle, status_code=201)
async def create_trace(payload: TraceEntry):
    """Ingest a single trace entry."""
    status_code, data = await request(
        LOGGER_TRACER_URL, "POST", "traces", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/batch", response_model=ApiResponseSingle, status_code=201)
async def create_traces_batch(payload: List[TraceEntry]):
    """Ingest multiple trace entries in a single request."""
    status_code, data = await request(
        LOGGER_TRACER_URL, "POST", "traces/batch", json=[item.model_dump(mode="json") for item in payload]
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
