"""
Dashboard Router
Endpoints for dashboard statistics and analytics
"""

from typing import Dict
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.mitarbeiter import Mitarbeiter, MitarbeiterStatus
from app.models.qualifikation import Qualifikation, MitarbeiterQualifikation
from app.models.verfuegbarkeit import Verfuegbarkeit, VerfuegbarkeitTyp
from app.schemas.ai_matching import DashboardStats
from app.services.auth import auth_service

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """
    Get dashboard statistics

    Returns:
    - Total employees
    - Available employees
    - Employees on assignment
    - Employees on vacation
    - Sick employees
    - Expiring certifications
    - Department distribution
    - Qualification distribution
    """
    # Total employees
    total_mitarbeiter = db.query(Mitarbeiter).count()

    # Available employees (aktiv status + not in current verfuegbarkeit)
    today = date.today()

    # Count by status
    verfuegbar_count = db.query(Mitarbeiter).filter(
        Mitarbeiter.status == MitarbeiterStatus.AKTIV
    ).count()

    # Count employees in different availability types (current)
    im_einsatz_count = db.query(Verfuegbarkeit).join(Mitarbeiter).filter(
        Verfuegbarkeit.typ == VerfuegbarkeitTyp.EINSATZ,
        Verfuegbarkeit.von_datum <= today,
        Verfuegbarkeit.bis_datum >= today
    ).distinct(Verfuegbarkeit.mitarbeiter_id).count()

    im_urlaub_count = db.query(Verfuegbarkeit).join(Mitarbeiter).filter(
        Verfuegbarkeit.typ == VerfuegbarkeitTyp.URLAUB,
        Verfuegbarkeit.von_datum <= today,
        Verfuegbarkeit.bis_datum >= today
    ).distinct(Verfuegbarkeit.mitarbeiter_id).count()

    krank_count = db.query(Verfuegbarkeit).join(Mitarbeiter).filter(
        Verfuegbarkeit.typ == VerfuegbarkeitTyp.KRANK,
        Verfuegbarkeit.von_datum <= today,
        Verfuegbarkeit.bis_datum >= today
    ).distinct(Verfuegbarkeit.mitarbeiter_id).count()

    # Expiring certifications (next 30 days)
    expiry_threshold = today + timedelta(days=30)
    ablaufende_zertifikate = db.query(MitarbeiterQualifikation).filter(
        MitarbeiterQualifikation.gueltig_bis.isnot(None),
        MitarbeiterQualifikation.gueltig_bis >= today,
        MitarbeiterQualifikation.gueltig_bis <= expiry_threshold
    ).count()

    # Department distribution
    abteilung_dist = db.query(
        Mitarbeiter.abteilung,
        func.count(Mitarbeiter.id).label('count')
    ).group_by(Mitarbeiter.abteilung).all()

    abteilung_distribution = {abt: count for abt, count in abteilung_dist}

    # Qualification distribution (top 10)
    qual_dist = db.query(
        Qualifikation.name,
        func.count(MitarbeiterQualifikation.id).label('count')
    ).join(MitarbeiterQualifikation).group_by(
        Qualifikation.name
    ).order_by(func.count(MitarbeiterQualifikation.id).desc()).limit(10).all()

    qualifikation_distribution = {qual: count for qual, count in qual_dist}

    return DashboardStats(
        total_mitarbeiter=total_mitarbeiter,
        verfuegbar=verfuegbar_count,
        im_einsatz=im_einsatz_count,
        im_urlaub=im_urlaub_count,
        krank=krank_count,
        ablaufende_zertifikate=ablaufende_zertifikate,
        abteilung_distribution=abteilung_distribution,
        qualifikation_distribution=qualifikation_distribution
    )


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """
    Get recent activity (latest created/updated employees)
    """
    recent_mitarbeiter = db.query(Mitarbeiter).order_by(
        Mitarbeiter.updated_at.desc()
    ).limit(limit).all()

    return {
        "recent_mitarbeiter": [
            {
                "id": m.id,
                "personal_nummer": m.personal_nummer,
                "full_name": m.full_name,
                "abteilung": m.abteilung,
                "updated_at": m.updated_at
            }
            for m in recent_mitarbeiter
        ]
    }
