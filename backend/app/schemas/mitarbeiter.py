"""
Mitarbeiter Schemas
Pydantic models for employee API
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

from app.models.mitarbeiter import MitarbeiterStatus


class MitarbeiterBase(BaseModel):
    """Base employee schema"""
    personal_nummer: str = Field(..., min_length=1, max_length=50)
    vorname: str = Field(..., min_length=1, max_length=100)
    nachname: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    abteilung: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=100)
    telefon: Optional[str] = Field(None, max_length=50)
    eintritt_datum: date
    status: MitarbeiterStatus = MitarbeiterStatus.AKTIV
    wochenstunden: Decimal = Field(default=Decimal("40.00"), ge=0, le=168)
    profilbild_url: Optional[str] = Field(None, max_length=500)


class MitarbeiterCreate(MitarbeiterBase):
    """Schema for creating employee"""
    pass


class MitarbeiterUpdate(BaseModel):
    """Schema for updating employee (all fields optional)"""
    vorname: Optional[str] = Field(None, min_length=1, max_length=100)
    nachname: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    abteilung: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    telefon: Optional[str] = Field(None, max_length=50)
    status: Optional[MitarbeiterStatus] = None
    wochenstunden: Optional[Decimal] = Field(None, ge=0, le=168)
    profilbild_url: Optional[str] = Field(None, max_length=500)


class MitarbeiterResponse(MitarbeiterBase):
    """Schema for employee response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MitarbeiterListResponse(BaseModel):
    """Schema for employee list response"""
    total: int
    items: List[MitarbeiterResponse]
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
