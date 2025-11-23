"""
Verfuegbarkeit Router
Endpoints for availability management
"""

from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.verfuegbarkeit import Verfuegbarkeit
from app.schemas.verfuegbarkeit import VerfuegbarkeitCreate, VerfuegbarkeitResponse
from app.services.auth import auth_service
from app.config import settings
from app.models.audit_log import AuditLog, AuditAction

router = APIRouter()


@router.get("/mitarbeiter/{mitarbeiter_id}", response_model=List[VerfuegbarkeitResponse])
async def get_mitarbeiter_verfuegbarkeit(
    mitarbeiter_id: int,
    from_date: date = Query(default=None),
    to_date: date = Query(default=None),
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Get availability for specific employee"""
    query = db.query(Verfuegbarkeit).filter(Verfuegbarkeit.mitarbeiter_id == mitarbeiter_id)

    if from_date:
        query = query.filter(Verfuegbarkeit.bis_datum >= from_date)
    if to_date:
        query = query.filter(Verfuegbarkeit.von_datum <= to_date)

    verfuegbarkeiten = query.order_by(Verfuegbarkeit.von_datum).all()
    return verfuegbarkeiten


@router.post("/", response_model=VerfuegbarkeitResponse, status_code=status.HTTP_201_CREATED)
async def create_verfuegbarkeit(
    verf_data: VerfuegbarkeitCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """Create new availability entry"""
    verfuegbarkeit = Verfuegbarkeit(**verf_data.model_dump())
    db.add(verfuegbarkeit)
    db.commit()
    db.refresh(verfuegbarkeit)

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.CREATE,
            entity_type="verfuegbarkeit",
            entity_id=verfuegbarkeit.id,
            changes=verf_data.model_dump()
        )

    return verfuegbarkeit


@router.delete("/{verfuegbarkeit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_verfuegbarkeit(
    verfuegbarkeit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.can_write)
):
    """Delete availability entry"""
    verfuegbarkeit = db.query(Verfuegbarkeit).filter(Verfuegbarkeit.id == verfuegbarkeit_id).first()

    if not verfuegbarkeit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability entry {verfuegbarkeit_id} not found"
        )

    if settings.ENABLE_AUDIT_LOG:
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            action=AuditAction.DELETE,
            entity_type="verfuegbarkeit",
            entity_id=verfuegbarkeit.id
        )

    db.delete(verfuegbarkeit)
    db.commit()

    return None
