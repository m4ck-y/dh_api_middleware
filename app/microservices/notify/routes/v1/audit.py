from fastapi import APIRouter, HTTPException, status, Query
from app.http_client import request
from app.settings import settings
from typing import List, Optional
from datetime import datetime
from app.microservices.notify.domain.models import MessageAuditEntry, MessageStatus

NOTIFY_URL = settings.SERVICE_NOTIFY_URL.rstrip("/")

router = APIRouter(prefix="/v1/audit", tags=["Audit"])

@router.get("/messages", response_model=List[MessageAuditEntry])
async def get_audit_logs(
    recipient: Optional[str] = Query(None, description="Filter by recipient email/phone"),
    status_filter: Optional[MessageStatus] = Query(None, alias="status", description="Filter by delivery status"),
    since: Optional[datetime] = Query(None, description="Show logs after this timestamp")
):
    """Retrieve filtered message dispatch logs."""
    params = {}
    if recipient:
        params["recipient"] = recipient
    if status_filter:
        params["status"] = status_filter.value
    if since:
        params["since"] = since.isoformat()
        
    status_code, data = await request(
        NOTIFY_URL, "GET", "v1/audit/messages", params=params
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.get("/health", summary="Audit Storage Health")
async def audit_health():
    """Verify audit storage connectivity."""
    status_code, data = await request(
        NOTIFY_URL, "GET", "v1/audit/health"
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
