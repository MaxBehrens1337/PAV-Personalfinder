"""
FastAPI Main Application
Entry point for PAV Personalfinder API
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.services.ai_matching import ai_matching_service

# Import routers
from app.routers import (
    auth_router,
    mitarbeiter_router,
    qualifikation_router,
    verfuegbarkeit_router,
    ai_matching_router,
    dashboard_router,
    user_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print("🚀 Starting PAV Personalfinder API...")

    # Initialize database
    print("📊 Initializing database...")
    init_db()

    # Initialize AI services (lazy)
    print("🤖 AI Matching Service ready (will initialize on first use)...")

    yield

    # Shutdown
    print("👋 Shutting down PAV Personalfinder API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered employee matching system for PAV",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Docker"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "PAV Personalfinder API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(mitarbeiter_router, prefix="/api/mitarbeiter", tags=["Mitarbeiter"])
app.include_router(qualifikation_router, prefix="/api/qualifikationen", tags=["Qualifikationen"])
app.include_router(verfuegbarkeit_router, prefix="/api/verfuegbarkeit", tags=["Verfügbarkeit"])
app.include_router(ai_matching_router, prefix="/api/ai-match", tags=["AI Matching"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    print(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
