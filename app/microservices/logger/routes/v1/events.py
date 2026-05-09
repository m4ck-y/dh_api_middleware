from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.http_client import request
from app.settings import settings
from app.shared.domain.api_response import ApiResponsePaginated, ApiResponseSingle
from app.microservices.logger.domain.models import EventEntry

LOGGER_URL = settings.SERVICE_LOGGER_URL.rstrip("/")

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=ApiResponsePaginated[EventEntry])
async def get_events(
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    page: int = Query(1, ge=1, description="Page number"),
    query: Optional[str] = Query(None, description="MongoDB style filter JSON (e.g. {'metadata.user':'123'})")
):
    """Retrieve historical business events."""
    params = {"limit": limit, "page": page}
    if query:
        params["query"] = query
        
    status_code, data = await request(
        LOGGER_URL, "GET", "events", params=params
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/", response_model=ApiResponseSingle, status_code=201)
async def create_event(payload: EventEntry):
    """Ingest a single high-level event."""
    status_code, data = await request(
        LOGGER_URL, "POST", "events", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
