from fastapi import APIRouter, HTTPException, status
from app.http_client import request
from app.settings import settings
from app.microservices.message_sender.domain.models import OTPRequest, WelcomeRequest, OTPResponse

MESSAGE_SENDER_URL = settings.SERVICE_MESSAGE_SENDER_URL.rstrip("/")

router = APIRouter(prefix="/emails", tags=["messages"])

@router.post("/send-otp", response_model=OTPResponse)
async def send_otp_code(payload: OTPRequest):
    """Dispatch an OTP verification code via the specified channel."""
    status_code, data = await request(
        MESSAGE_SENDER_URL, "POST", "emails/send-otp", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/welcome", response_model=OTPResponse)
async def send_welcome_message(payload: WelcomeRequest):
    """Dispatch a personalized welcome message to a new user."""
    status_code, data = await request(
        MESSAGE_SENDER_URL, "POST", "emails/welcome", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/send-otp-legacy")
async def send_otp_legacy(email: str, code: str):
    """Legacy compatibility endpoint for OTP dispatch."""
    status_code, data = await request(
        MESSAGE_SENDER_URL, "POST", f"emails/send-otp-legacy?email={email}&code={code}"
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
