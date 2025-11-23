"""
Qualifikation Schemas
Pydantic models for qualification API
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

from app.models.qualifikation import QualifikationKategorie, QualifikationLevel


class QualifikationBase(BaseModel):
    """Base qualification schema"""
    name: str = Field(..., min_length=1, max_length=200)
    kategorie: QualifikationKategorie
    beschreibung: Optional[str] = None


class QualifikationCreate(QualifikationBase):
    """Schema for creating qualification"""
    pass


class QualifikationResponse(QualifikationBase):
    """Schema for qualification response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MitarbeiterQualifikationBase(BaseModel):
    """Base employee-qualification association schema"""
    qualifikation_id: int
    level: QualifikationLevel = QualifikationLevel.FORTGESCHRITTEN
    gueltig_von: Optional[date] = None
    gueltig_bis: Optional[date] = None
    notizen: Optional[str] = None


class MitarbeiterQualifikationCreate(MitarbeiterQualifikationBase):
    """Schema for creating employee-qualification association"""
    pass


class MitarbeiterQualifikationResponse(BaseModel):
    """Schema for employee-qualification response"""
    id: int
    mitarbeiter_id: int
    qualifikation: QualifikationResponse
    level: QualifikationLevel
    gueltig_von: Optional[date]
    gueltig_bis: Optional[date]
    notizen: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
