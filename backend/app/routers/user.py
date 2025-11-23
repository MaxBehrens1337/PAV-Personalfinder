"""
User Router
Endpoints for user management
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.auth import auth_service
from app.config import settings
from app.models.audit_log import AuditLog, AuditAction

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.is_admin)
):
    """
    List all users
    Requires: ADMIN role
    """
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.is_admin)
):
    """
    Get user by ID
    Requires: ADMIN role
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.is_admin)
):
    """
    Create new user
    Requires: ADMIN role
    """
    # Check if username already exists
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{user_data.username}' already exists"
        )

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user_data.email}' already exists"
        )

    # Hash password
    user_dict = user_data.model_dump()
    password = user_dict.pop("password")
    password_hash = auth_service.hash_password(password)

    # Create user
    user = User(**user_dict, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.CREATE,
            entity_type="user",
            entity_id=user.id,
            changes={"username": user.username, "email": user.email, "rolle": user.rolle.value}
        )

    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.is_admin)
):
    """
    Update user
    Requires: ADMIN role
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)

    # Handle password separately
    if "password" in update_data:
        password = update_data.pop("password")
        update_data["password_hash"] = auth_service.hash_password(password)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.UPDATE,
            entity_type="user",
            entity_id=user.id,
            changes={k: v for k, v in update_data.items() if k != "password_hash"}
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.is_admin)
):
    """
    Delete user
    Requires: ADMIN role
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own user account"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.DELETE,
            entity_type="user",
            entity_id=user.id,
            changes={"username": user.username}
        )

    db.delete(user)
    db.commit()

    return None
