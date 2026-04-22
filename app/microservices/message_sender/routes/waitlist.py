from fastapi import APIRouter, HTTPException, status
from app.http_client import request
from app.settings import settings
from app.microservices.message_sender.domain.models import WaitlistRequest, WaitlistResponse

MESSAGE_SENDER_URL = settings.SERVICE_MESSAGE_SENDER_URL.rstrip("/")

router = APIRouter(prefix="/waitlist", tags=["Waitlist Notifications"])

@router.post("/send-confirmation", response_model=WaitlistResponse)
async def send_waitlist_confirmation(payload: WaitlistRequest):
    """Dispatch a waitlist registration confirmation."""
    status_code, data = await request(
        MESSAGE_SENDER_URL, "POST", "waitlist/send-confirmation", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
