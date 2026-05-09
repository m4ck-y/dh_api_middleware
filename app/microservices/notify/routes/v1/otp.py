from fastapi import APIRouter, HTTPException, status
from app.http_client import request
from app.settings import settings
from app.microservices.notify.domain.models import OTPRequest, WelcomeRequest, OTPResponse

NOTIFY_URL = settings.SERVICE_NOTIFY_URL.rstrip("/")

router = APIRouter(prefix="/v1", tags=["messages"])

@router.post("/otp", response_model=OTPResponse)
async def send_otp_code(payload: OTPRequest):
    """Dispatch an OTP verification code via the specified channel."""
    status_code, data = await request(
        NOTIFY_URL, "POST", "v1/otp", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/applicant/welcome", response_model=OTPResponse)
async def send_welcome_message(payload: WelcomeRequest):
    """Dispatch a personalized welcome message to a new applicant."""
    status_code, data = await request(
        NOTIFY_URL, "POST", "v1/applicant/welcome", json=payload.model_dump(mode="json")
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data

@router.post("/otp-legacy")
async def send_otp_legacy(email: str, code: str):
    """Legacy compatibility endpoint for OTP dispatch."""
    status_code, data = await request(
        NOTIFY_URL, "POST", f"v1/otp-legacy?email={email}&code={code}"
    )
    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=data)
    return data
