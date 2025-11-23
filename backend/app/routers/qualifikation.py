"""
Qualifikation Router
Endpoints for qualification management
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.qualifikation import Qualifikation, MitarbeiterQualifikation
from app.schemas.qualifikation import (
    QualifikationCreate,
    QualifikationResponse,
    MitarbeiterQualifikationCreate,
    MitarbeiterQualifikationResponse,
)
from app.services.auth import auth_service
from app.config import settings
from app.models.audit_log import AuditLog, AuditAction

router = APIRouter()


@router.get("/", response_model=List[QualifikationResponse])
async def list_qualifikationen(
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """List all qualifications"""
    qualifikationen = db.query(Qualifikation).all()
    return qualifikationen


@router.post("/", response_model=QualifikationResponse, status_code=status.HTTP_201_CREATED)
async def create_qualifikation(
    qual_data: QualifikationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """Create new qualification"""
    # Check if exists
    existing = db.query(Qualifikation).filter(Qualifikation.name == qual_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Qualification '{qual_data.name}' already exists"
        )

    qualifikation = Qualifikation(**qual_data.model_dump())
    db.add(qualifikation)
    db.commit()
    db.refresh(qualifikation)

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.CREATE,
            entity_type="qualifikation",
            entity_id=qualifikation.id,
            changes=qual_data.model_dump()
        )

    return qualifikation


@router.post("/mitarbeiter/{mitarbeiter_id}", response_model=MitarbeiterQualifikationResponse)
async def add_qualifikation_to_mitarbeiter(
    mitarbeiter_id: int,
    qual_data: MitarbeiterQualifikationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """Add qualification to employee"""
    mq = MitarbeiterQualifikation(
        mitarbeiter_id=mitarbeiter_id,
        **qual_data.model_dump()
    )
    db.add(mq)
    db.commit()
    db.refresh(mq)

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.CREATE,
            entity_type="mitarbeiter_qualifikation",
            entity_id=mq.id,
            changes={"mitarbeiter_id": mitarbeiter_id, **qual_data.model_dump()}
        )

    return mq
