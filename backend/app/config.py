"""
Configuration Module
Handles all application settings and environment variables
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application Settings"""

    # Application
    APP_NAME: str = "PAV Personalfinder"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # AI/ML Configuration
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "employee_profiles"

    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_TIMEOUT: int = 60

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # Feature Flags
    ENABLE_AI_MATCHING: bool = True
    ENABLE_AUDIT_LOG: bool = True

    # Performance & Limits
    MAX_SEARCH_RESULTS: int = 50
    AI_MATCHING_TIMEOUT: int = 10
    RATE_LIMIT_PER_MINUTE: int = 60

    # DSGVO / Privacy
    DATA_RETENTION_DAYS: int = 2555  # ~7 Jahre
    AUDIT_LOG_RETENTION_DAYS: int = 3650  # 10 Jahre

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
