"""API Routers module."""

from src.api.routers.auth import router as auth_router
from src.api.routers.health import router as health_router

__all__ = ["auth_router", "health_router"]
