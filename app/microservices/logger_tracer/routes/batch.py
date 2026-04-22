from fastapi import APIRouter, HTTPException, status
from app.http_client import request
from app.settings import settings
from app.microservices.logger_tracer.domain.models import BatchEntry

LOGGER_TRACER_URL = settings.SERVICE_LOGGER_TRACER_URL.rstrip("/")

router = APIRouter(prefix="/batch", tags=["Batch"])

@router.post("/", status_code=201)
async def create_batch(payload: BatchEntry):
    """Ingest mixed telemetry signals in a single batch."""
    status_code, data = await request(
        LOGGER_TRACER_URL, "POST", "batch", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
