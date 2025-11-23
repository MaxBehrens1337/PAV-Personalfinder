"""
AI Matching Router
Endpoints for AI-powered employee matching
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ai_matching import AIMatchRequest, AIMatchResponse
from app.services.auth import auth_service
from app.services.ai_matching import ai_matching_service
from app.models.audit_log import AuditLog, AuditAction
from app.config import settings

router = APIRouter()


@router.post("/search", response_model=AIMatchResponse)
async def ai_match_search(
    request: AIMatchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """
    AI-powered employee matching

    This endpoint uses semantic search with Qdrant and LLM evaluation with Ollama
    to find and rank the best matching employees for given requirements.

    Falls back to classical search if AI services are unavailable.
    """
    # Log search action
    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.SEARCH,
            entity_type="ai_matching",
            changes={
                "query": request.query,
                "use_ai": request.use_ai,
                "max_results": request.max_results
            }
        )

    # Perform AI matching
    try:
        response = await ai_matching_service.match_employees(request, db)
        return response

    except Exception as e:
        print(f"Error in AI matching: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing AI matching: {str(e)}"
        )


@router.post("/reindex")
async def reindex_all_employees(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.is_admin)
):
    """
    Re-index all employees in Qdrant vector database

    This endpoint triggers a background task to re-index all employees.
    Useful after bulk imports or data migrations.

    Requires: ADMIN role
    """
    def reindex_task():
        """Background task to reindex employees"""
        ai_matching_service.index_all_mitarbeiter(db)

    background_tasks.add_task(reindex_task)

    return {
        "message": "Re-indexing started in background",
        "status": "processing"
    }


@router.get("/status")
async def ai_service_status(
    current_user = Depends(auth_service.get_current_user)
):
    """
    Get AI service status

    Returns information about AI services availability
    """
    return {
        "ai_matching_enabled": settings.ENABLE_AI_MATCHING,
        "ai_initialized": ai_matching_service._initialized,
        "ollama_host": settings.OLLAMA_HOST,
        "ollama_model": settings.OLLAMA_MODEL,
        "qdrant_host": settings.QDRANT_HOST,
        "qdrant_collection": settings.QDRANT_COLLECTION_NAME,
        "embedding_model": settings.EMBEDDING_MODEL,
    }
