"""
Suchanfrage Schemas
Pydantic models for saved searches API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SuchanfrageBase(BaseModel):
    """Base saved search schema"""
    name: str = Field(..., min_length=1, max_length=200)
    query_text: str = Field(..., min_length=1)
    filter_params: Optional[Dict[str, Any]] = None


class SuchanfrageCreate(SuchanfrageBase):
    """Schema for creating saved search"""
    pass


class SuchanfrageUpdate(BaseModel):
    """Schema for updating saved search"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    query_text: Optional[str] = Field(None, min_length=1)
    filter_params: Optional[Dict[str, Any]] = None


class SuchanfrageResponse(SuchanfrageBase):
    """Schema for saved search response"""
    id: int
    user_id: int
    created_at: datetime
    last_used_at: Optional[datetime]
    use_count: int

    class Config:
        from_attributes = True
