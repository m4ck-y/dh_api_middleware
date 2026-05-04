"""Onboarding proxy endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from uuid import UUID

from app.http_client import request
from app.microservices.onboarding.app import ONBOARDING_URL
from app.microservices.onboarding.domain import (
    AddressDTO,
    ApiResponseSingle,
    DocumentResponseDTO,
    EDocumentSide,
    OnboardingResponseDTO,
    OnboardingStartDTO,
    OnboardingStartResponseDTO,
    OtpSendDTO,
    OtpSentResponseDTO,
    OtpVerifyDTO,
    PasswordSetupDTO,
    PersonalInfoDTO,
)

router = APIRouter(tags=["Onboarding"])


@router.post("/start", response_model=ApiResponseSingle[OnboardingStartResponseDTO])
async def start_onboarding(payload: OnboardingStartDTO):
    status, data = await request(ONBOARDING_URL, "POST", "v1/onboarding/start", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/personal-info", response_model=ApiResponseSingle[OnboardingResponseDTO], status_code=201)
async def save_personal_info(payload: PersonalInfoDTO):
    status, data = await request(ONBOARDING_URL, "POST", "v1/onboarding/personal-info", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_person}/otp/send", response_model=ApiResponseSingle[OtpSentResponseDTO])
async def send_otp(uuid_person: str, payload: OtpSendDTO):
    status, data = await request(ONBOARDING_URL, "POST", f"v1/onboarding/{uuid_person}/otp/send", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_person}/otp/verify", response_model=ApiResponseSingle[OnboardingResponseDTO])
async def verify_otp(uuid_person: str, payload: OtpVerifyDTO):
    status, data = await request(ONBOARDING_URL, "POST", f"v1/onboarding/{uuid_person}/otp/verify", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_person}/password", response_model=ApiResponseSingle[OnboardingResponseDTO])
async def set_password(uuid_person: str, payload: PasswordSetupDTO):
    status, data = await request(ONBOARDING_URL, "POST", f"v1/onboarding/{uuid_person}/password", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_person}/address", response_model=ApiResponseSingle[OnboardingResponseDTO])
async def save_address(uuid_person: str, payload: AddressDTO):
    status, data = await request(ONBOARDING_URL, "POST", f"v1/onboarding/{uuid_person}/address", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_person}/documents", response_model=ApiResponseSingle[DocumentResponseDTO], status_code=201)
async def upload_document(
    uuid_person: str,
    uuid_document_subtype: UUID = Form(...),
    title: str | None = Form(None),
    files: List[UploadFile] = File(...),
    sides: List[EDocumentSide] = Form(...),
):
    form_data: dict = {"uuid_document_subtype": str(uuid_document_subtype)}
    if title is not None:
        form_data["title"] = title
    form_data["sides"] = [s.value for s in sides]

    upload_files: list = []
    for i, f in enumerate(files):
        content = await f.read()
        upload_files.append(("files", (f.filename, content, f.content_type or "application/octet-stream")))

    status, data = await request(
        ONBOARDING_URL, "POST", f"v1/onboarding/{uuid_person}/documents",
        data=form_data,
        files=upload_files,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/{uuid_person}/submit", response_model=ApiResponseSingle[OnboardingResponseDTO])
async def submit_onboarding(uuid_person: str):
    status, data = await request(ONBOARDING_URL, "POST", f"v1/onboarding/{uuid_person}/submit")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
