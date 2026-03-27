"""Which headers are safe to copy across the gateway boundary."""

from __future__ import annotations

from typing import Mapping

_HOP_BY_HOP_REQUEST = frozenset(
    k.lower()
    for k in (
        "Connection",
        "Keep-Alive",
        "Proxy-Authenticate",
        "Proxy-Authorization",
        "TE",
        "Trailers",
        "Transfer-Encoding",
        "Upgrade",
        "Host",
    )
)

_SKIP_RESPONSE = frozenset(
    k.lower()
    for k in (
        "Connection",
        "Keep-Alive",
        "Proxy-Authenticate",
        "Proxy-Authorization",
        "TE",
        "Trailers",
        "Transfer-Encoding",
        "Upgrade",
        "Content-Length",
    )
)


def filter_request_headers(headers: Mapping[str, str]) -> dict[str, str]:
    """Drop hop-by-hop headers before calling the Health Monitoring backend."""
    return {k: v for k, v in headers.items() if k.lower() not in _HOP_BY_HOP_REQUEST}


def filter_response_headers(headers: Mapping[str, str]) -> dict[str, str]:
    """Drop hop-by-hop and length headers when building the client response."""
    return {k: v for k, v in headers.items() if k.lower() not in _SKIP_RESPONSE}
