"""API Gateway application."""

from app.http_client import request
from app.settings import settings

__all__ = ["request", "settings"]
