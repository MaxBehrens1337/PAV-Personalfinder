"""
API Routers
All API endpoint routers
"""

from .auth import router as auth_router
from .mitarbeiter import router as mitarbeiter_router
from .qualifikation import router as qualifikation_router
from .verfuegbarkeit import router as verfuegbarkeit_router
from .ai_matching import router as ai_matching_router
from .dashboard import router as dashboard_router
from .user import router as user_router

__all__ = [
    "auth_router",
    "mitarbeiter_router",
    "qualifikation_router",
    "verfuegbarkeit_router",
    "ai_matching_router",
    "dashboard_router",
    "user_router",
]
