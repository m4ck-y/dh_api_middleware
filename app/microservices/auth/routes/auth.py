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
    UserInfoDTO,
)
from app.shared.domain import ApiResponseSingle

router = APIRouter()


def _cookie_header(req: Request) -> dict[str, str]:
    cookie = req.headers.get("cookie", "")
    return {"Cookie": cookie} if cookie else {}


@router.post("/login", response_model=ApiResponseSingle[LoginResponseDTO])
async def login(payload: LoginRequestDTO, req: Request):
    """
    Authenticate a user and issue access + refresh tokens.

    Validates credentials against AuthUser table, fetches roles/permissions
    from IAM service, and sets two HttpOnly cookies:
    - `access_token`: JWT with user claims (15 min default).
    - `refresh_token`: Random token stored in Session table (30 days default).

    Returns 401 for invalid credentials and 403 for inactive users.
    """
    status, data = await request(
        AUTH_URL, "POST", "v1/auth/login",
        json=payload.model_dump(),
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/refresh", response_model=ApiResponseSingle[MessageResponseDTO])
async def refresh(req: Request):
    """
    Refresh the access token using a valid refresh token.

    Reads the `refresh_token` cookie, validates it against the Session table,
    fetches updated roles/permissions from IAM, and issues a new access_token cookie.

    Returns 401 if the refresh token is missing, expired, or invalid.
    """
    status, data = await request(
        AUTH_URL, "POST", "v1/auth/refresh",
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/logout", response_model=ApiResponseSingle[MessageResponseDTO])
async def logout(req: Request):
    """
    Log out the current user by deleting the auth cookies.

    Clears both `access_token` and `refresh_token` cookies from the client.
    Does not invalidate the server-side session (TTL-based expiration).
    """
    status, data = await request(
        AUTH_URL, "POST", "v1/auth/logout",
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/me", response_model=ApiResponseSingle[MeResponseDTO])
async def get_me(req: Request):
    """
    Get the current authenticated user's profile.

    Reads the `access_token` cookie, decodes the JWT, and fetches the full
    profile (person info, employee/company, tenants, roles, permissions).

    Returns 401 if the token is missing, expired, or invalid.
    Returns 404 if the user profile is not found in the database.
    """
    status, data = await request(
        AUTH_URL, "GET", "v1/auth/me",
        headers=_cookie_header(req),
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
