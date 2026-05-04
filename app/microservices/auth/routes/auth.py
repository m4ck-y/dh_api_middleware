"""Auth routes - proxy to dh_auth backend."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.http_client import request
from app.microservices.auth.app import AUTH_URL
from app.microservices.auth.domain.auth_dto import (
    LoginRequestDTO,
    LoginResponseDTO,
    MeResponseDTO,
    MessageResponseDTO,
)
from app.shared.domain import ApiResponseSingle

router = APIRouter()


def _cookie_header(req: Request) -> dict[str, str]:
    cookie = req.headers.get("cookie", "")
    return {"Cookie": cookie} if cookie else {}


@router.post("/login", response_model=ApiResponseSingle[LoginResponseDTO])
async def login(payload: LoginRequestDTO, req: Request):
    status, data = await request(
        AUTH_URL, "POST", "v1/auth/login",
        json=payload.model_dump(),
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/silent-refresh", response_model=ApiResponseSingle[MessageResponseDTO])
async def silent_refresh(req: Request):
    status, data = await request(
        AUTH_URL, "POST", "v1/auth/refresh",
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/logout", response_model=ApiResponseSingle[MessageResponseDTO])
async def logout(req: Request):
    status, data = await request(
        AUTH_URL, "POST", "v1/auth/logout",
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/me", response_model=ApiResponseSingle[MeResponseDTO])
async def get_me(req: Request):
    status, data = await request(
        AUTH_URL, "GET", "v1/auth/me",
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
