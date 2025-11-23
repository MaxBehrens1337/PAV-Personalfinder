"""
Verfuegbarkeit Schemas
Pydantic models for availability API
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime

from app.models.verfuegbarkeit import VerfuegbarkeitTyp


class VerfuegbarkeitBase(BaseModel):
    """Base availability schema"""
    typ: VerfuegbarkeitTyp
    von_datum: date
    bis_datum: date
    notizen: Optional[str] = None

    @field_validator('bis_datum')
    @classmethod
    def validate_date_range(cls, v, info):
        if 'von_datum' in info.data and v < info.data['von_datum']:
            raise ValueError('bis_datum must be after von_datum')
        return v


class VerfuegbarkeitCreate(VerfuegbarkeitBase):
    """Schema for creating availability"""
    mitarbeiter_id: int


class VerfuegbarkeitResponse(VerfuegbarkeitBase):
    """Schema for availability response"""
    id: int
    mitarbeiter_id: int
    created_at: datetime

    class Config:
        from_attributes = True
