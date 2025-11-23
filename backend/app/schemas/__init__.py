"""
Pydantic Schemas for API validation and serialization
"""

from .mitarbeiter import (
    MitarbeiterBase,
    MitarbeiterCreate,
    MitarbeiterUpdate,
    MitarbeiterResponse,
    MitarbeiterListResponse,
)
from .qualifikation import (
    QualifikationBase,
    QualifikationCreate,
    QualifikationResponse,
    MitarbeiterQualifikationCreate,
    MitarbeiterQualifikationResponse,
)
from .verfuegbarkeit import (
    VerfuegbarkeitBase,
    VerfuegbarkeitCreate,
    VerfuegbarkeitResponse,
)
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
)
from .suchanfrage import (
    SuchanfrageCreate,
    SuchanfrageResponse,
)
from .ai_matching import (
    AIMatchRequest,
    AIMatchResult,
    AIMatchResponse,
)

__all__ = [
    # Mitarbeiter
    "MitarbeiterBase",
    "MitarbeiterCreate",
    "MitarbeiterUpdate",
    "MitarbeiterResponse",
    "MitarbeiterListResponse",
    # Qualifikation
    "QualifikationBase",
    "QualifikationCreate",
    "QualifikationResponse",
    "MitarbeiterQualifikationCreate",
    "MitarbeiterQualifikationResponse",
    # Verfuegbarkeit
    "VerfuegbarkeitBase",
    "VerfuegbarkeitCreate",
    "VerfuegbarkeitResponse",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    # Suchanfrage
    "SuchanfrageCreate",
    "SuchanfrageResponse",
    # AI Matching
    "AIMatchRequest",
    "AIMatchResult",
    "AIMatchResponse",
]
