"""Units endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from health_monitoring_gateway.domain.schemas import (
    UnitCreate,
    UnitRead,
    CountResponse,
    MessageResponse,
)
from health_monitoring_gateway.infrastructure.http_client import request

router = APIRouter(tags=["Units"])


@router.get("/units", response_model=list[UnitRead])
async def list_units():
    status, data = await request("GET", "units")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/units/count", response_model=CountResponse)
async def units_count():
    status, data = await request("GET", "units/count")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/units/{unit_id}", response_model=UnitRead)
async def get_unit(unit_id: int):
    status, data = await request("GET", f"units/{unit_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/units", response_model=UnitRead, status_code=201)
async def create_unit(payload: UnitCreate):
    status, data = await request("POST", "units", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.put("/units/{unit_id}", response_model=UnitRead)
async def update_unit(unit_id: int, payload: UnitCreate):
    status, data = await request("PUT", f"units/{unit_id}", json=payload.model_dump())
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.patch("/units/{unit_id}", response_model=UnitRead)
async def patch_unit(unit_id: int, payload: UnitCreate):
    status, data = await request(
        "PATCH", f"units/{unit_id}", json=payload.model_dump(exclude_unset=True)
    )
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.delete("/units/{unit_id}", response_model=MessageResponse)
async def delete_unit(unit_id: int):
    status, data = await request("DELETE", f"units/{unit_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
