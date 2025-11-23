"""
Authentication Router
Endpoints for user authentication
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.schemas.user import Token, UserLogin
from app.services.auth import auth_service
from app.models.audit_log import AuditLog, AuditAction

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint
    Returns JWT access token
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        # Log failed login attempt
        if settings.ENABLE_AUDIT_LOG:
            AuditLog.log_action(
                db=db,
                user_id=None,
                action=AuditAction.LOGIN,
                changes={"success": False, "username": form_data.username}
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Log successful login
    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=user.id,
            action=AuditAction.LOGIN,
            changes={"success": True}
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "user_id": user.id, "rolle": user.rolle.value},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    current_user = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout endpoint
    (Client should discard the token)
    """
    # Log logout
    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.LOGOUT
        )

    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user_info(
    current_user = Depends(auth_service.get_current_user)
):
    """
    Get current user information
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "rolle": current_user.rolle.value,
        "is_active": current_user.is_active,
    }
