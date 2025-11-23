"""
Mitarbeiter Router
Endpoints for employee management (CRUD)
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.mitarbeiter import Mitarbeiter, MitarbeiterStatus
from app.models.audit_log import AuditLog, AuditAction
from app.schemas.mitarbeiter import (
    MitarbeiterCreate,
    MitarbeiterUpdate,
    MitarbeiterResponse,
    MitarbeiterListResponse,
)
from app.services.auth import auth_service
from app.services.ai_matching import ai_matching_service
from app.config import settings

router = APIRouter()


@router.get("/", response_model=MitarbeiterListResponse)
async def list_mitarbeiter(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: Optional[str] = None,
    abteilung: Optional[str] = None,
    status: Optional[MitarbeiterStatus] = None,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """
    List all employees with pagination and filters
    """
    query = db.query(Mitarbeiter)

    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Mitarbeiter.vorname.ilike(search_term),
                Mitarbeiter.nachname.ilike(search_term),
                Mitarbeiter.personal_nummer.ilike(search_term),
                Mitarbeiter.email.ilike(search_term)
            )
        )

    if abteilung:
        query = query.filter(Mitarbeiter.abteilung == abteilung)

    if status:
        query = query.filter(Mitarbeiter.status == status)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    total_pages = (total + page_size - 1) // page_size

    return MitarbeiterListResponse(
        total=total,
        items=items,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{mitarbeiter_id}", response_model=MitarbeiterResponse)
async def get_mitarbeiter(
    mitarbeiter_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """
    Get employee by ID
    """
    mitarbeiter = db.query(Mitarbeiter).filter(Mitarbeiter.id == mitarbeiter_id).first()

    if not mitarbeiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {mitarbeiter_id} not found"
        )

    return mitarbeiter


@router.post("/", response_model=MitarbeiterResponse, status_code=status.HTTP_201_CREATED)
async def create_mitarbeiter(
    mitarbeiter_data: MitarbeiterCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """
    Create new employee
    Requires: USER or ADMIN role
    """
    # Check if personal_nummer already exists
    existing = db.query(Mitarbeiter).filter(
        Mitarbeiter.personal_nummer == mitarbeiter_data.personal_nummer
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with personal number {mitarbeiter_data.personal_nummer} already exists"
        )

    # Check if email already exists
    existing_email = db.query(Mitarbeiter).filter(
        Mitarbeiter.email == mitarbeiter_data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with email {mitarbeiter_data.email} already exists"
        )

    # Create employee
    mitarbeiter = Mitarbeiter(**mitarbeiter_data.model_dump())
    db.add(mitarbeiter)
    db.commit()
    db.refresh(mitarbeiter)

    # Log action
    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.CREATE,
            entity_type="mitarbeiter",
            entity_id=mitarbeiter.id,
            changes=mitarbeiter_data.model_dump()
        )

    # Index in Qdrant for AI matching
    if settings.ENABLE_AI_MATCHING:
        try:
            ai_matching_service.index_mitarbeiter(db, mitarbeiter.id)
        except Exception as e:
            print(f"Warning: Failed to index employee in Qdrant: {e}")

    return mitarbeiter


@router.patch("/{mitarbeiter_id}", response_model=MitarbeiterResponse)
async def update_mitarbeiter(
    mitarbeiter_id: int,
    mitarbeiter_data: MitarbeiterUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """
    Update employee
    Requires: USER or ADMIN role
    """
    mitarbeiter = db.query(Mitarbeiter).filter(Mitarbeiter.id == mitarbeiter_id).first()

    if not mitarbeiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {mitarbeiter_id} not found"
        )

    # Update fields
    update_data = mitarbeiter_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(mitarbeiter, field, value)

    db.commit()
    db.refresh(mitarbeiter)

    # Log action
    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.UPDATE,
            entity_type="mitarbeiter",
            entity_id=mitarbeiter.id,
            changes=update_data
        )

    # Re-index in Qdrant
    if settings.ENABLE_AI_MATCHING:
        try:
            ai_matching_service.index_mitarbeiter(db, mitarbeiter.id)
        except Exception as e:
            print(f"Warning: Failed to re-index employee in Qdrant: {e}")

    return mitarbeiter


@router.delete("/{mitarbeiter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mitarbeiter(
    mitarbeiter_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """
    Delete employee
    Requires: USER or ADMIN role
    """
    mitarbeiter = db.query(Mitarbeiter).filter(Mitarbeiter.id == mitarbeiter_id).first()

    if not mitarbeiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {mitarbeiter_id} not found"
        )

    # Log action before deletion
    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.DELETE,
            entity_type="mitarbeiter",
            entity_id=mitarbeiter.id,
            changes={"personal_nummer": mitarbeiter.personal_nummer, "name": mitarbeiter.full_name}
        )

    db.delete(mitarbeiter)
    db.commit()

    return None
