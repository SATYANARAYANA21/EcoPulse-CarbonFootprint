"""
Rate limiting configuration using slowapi (Starlette-compatible wrapper for limits).

The limiter uses the client's real IP address as the rate-limit key.
Limits are defined as constants so routes can reference them by name.
"""

from __future__ import annotations

from fastapi import Request
from slowapi import Limiter


def get_real_ip(request: Request) -> str:
    """Safely extract the real client IP behind proxies (e.g., Vercel)."""
    if "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"].split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


# Shared limiter instance — must be attached to app.state.limiter in main.py
limiter = Limiter(key_func=get_real_ip)

# Per-route rate limit strings (requests/minute)
CALCULATE_LIMIT = "30/minute"
INSIGHTS_LIMIT = "10/minute"
ENTRIES_LIMIT = "20/minute"
