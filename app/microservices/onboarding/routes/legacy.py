"""Legacy onboarding proxy endpoints."""

from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from uuid import UUID

from app.http_client import request
from app.microservices.onboarding.app import ONBOARDING_URL
from app.microservices.onboarding.domain import (
    ApiResponseSingle,
    LegacyCurpBody,
    LegacyDireccionBody,
    LegacyRegistroBody,
)

router = APIRouter(tags=["Onboarding — Legacy"])


@router.post("/preregistro/registro", response_model=ApiResponseSingle, status_code=201)
async def legacy_registro(payload: LegacyRegistroBody):
    status, data = await request(ONBOARDING_URL, "POST", "v1/onboarding/legacy/preregistro/registro", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/curp/subir", response_model=ApiResponseSingle)
async def legacy_guardar_curp(uuid_person: str, payload: LegacyCurpBody):
    status, data = await request(ONBOARDING_URL, "POST", "v1/onboarding/legacy/curp/subir", params={"uuid_person": uuid_person}, json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/direccion/guardar", response_model=ApiResponseSingle)
async def legacy_guardar_direccion(uuid_person: str, payload: LegacyDireccionBody):
    status, data = await request(ONBOARDING_URL, "POST", "v1/onboarding/legacy/direccion/guardar", params={"uuid_person": uuid_person}, json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/ine/subir-pdf", response_model=ApiResponseSingle, status_code=201)
async def legacy_subir_ine(
    uuid_person: str,
    uuid_document_subtype_ine: UUID = Form(...),
    file: UploadFile = File(...),
):
    content = await file.read()
    upload_files = [("file", (file.filename, content, file.content_type or "application/octet-stream"))]
    status, data = await request(
        ONBOARDING_URL, "POST",
        "v1/onboarding/legacy/ine/subir-pdf",
        params={"uuid_person": uuid_person},
        data={"uuid_document_subtype_ine": str(uuid_document_subtype_ine)},
        files=upload_files,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/comprobante/subir", response_model=ApiResponseSingle, status_code=201)
async def legacy_subir_comprobante(
    uuid_person: str,
    uuid_document_subtype_proof: UUID = Form(...),
    file: UploadFile = File(...),
):
    content = await file.read()
    upload_files = [("file", (file.filename, content, file.content_type or "application/octet-stream"))]
    status, data = await request(
        ONBOARDING_URL, "POST",
        "v1/onboarding/legacy/comprobante/subir",
        params={"uuid_person": uuid_person},
        data={"uuid_document_subtype_proof": str(uuid_document_subtype_proof)},
        files=upload_files,
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
