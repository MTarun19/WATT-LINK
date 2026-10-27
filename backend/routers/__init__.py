"""
WATT LINK Routers Package
-------------------------
This package contains all FastAPI routers.
"""

from .auth_router import router as auth_router
from .profile_router import router as profile_router
from .sensor_router import router as sensor_router
from .ai_router import router as ai_router
from .marketplace_router import router as marketplace_router
from .relay_router import router as relay_router
from .battery_router import router as battery_router

__all__ = [
    "auth_router",
    "profile_router",
    "sensor_router",
    "ai_router",
    "marketplace_router",
    "relay_router",
    "battery_router",
]