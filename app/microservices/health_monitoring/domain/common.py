"""Common response schemas."""

from pydantic import BaseModel


class CountResponse(BaseModel):
    count: int


class MessageResponse(BaseModel):
    message: str


class BackendHealthStatusResponse(BaseModel):
    status: str


class BackendVersionResponse(BaseModel):
    version: str


class JsonObjectResponse(BaseModel):
    data: dict
