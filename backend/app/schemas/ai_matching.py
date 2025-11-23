"""
AI Matching Schemas
Pydantic models for AI-powered employee matching
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AIMatchRequest(BaseModel):
    """Schema for AI matching request"""
    query: str = Field(..., min_length=1, description="Natural language query describing requirements")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of results to return")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Additional filters (abteilung, status, etc.)")
    use_ai: bool = Field(default=True, description="Use AI matching or fall back to classical search")


class AIMatchResult(BaseModel):
    """Schema for individual match result"""
    mitarbeiter_id: int
    personal_nummer: str
    full_name: str
    abteilung: str
    position: str
    email: str
    status: str
    match_score: float = Field(..., ge=0.0, le=100.0, description="Match score percentage (0-100)")
    reasoning: str = Field(..., description="AI-generated explanation for the match")
    strengths: List[str] = Field(default_factory=list, description="Key strengths/matching points")
    gaps: Optional[List[str]] = Field(default=None, description="Potential gaps or areas of concern")
    qualifikationen: List[str] = Field(default_factory=list, description="Relevant qualifications")


class AIMatchResponse(BaseModel):
    """Schema for AI matching response"""
    query: str
    total_matches: int
    ai_enabled: bool
    matches: List[AIMatchResult]
    execution_time_seconds: float
    timestamp: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    total_mitarbeiter: int
    verfuegbar: int
    im_einsatz: int
    im_urlaub: int
    krank: int
    ablaufende_zertifikate: int
    abteilung_distribution: Dict[str, int]
    qualifikation_distribution: Dict[str, int]

    class Config:
        from_attributes = True
