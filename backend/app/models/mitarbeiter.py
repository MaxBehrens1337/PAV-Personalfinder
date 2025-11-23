"""
Mitarbeiter Model
Employee database model
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base


class MitarbeiterStatus(str, enum.Enum):
    """Employee status enum"""
    AKTIV = "aktiv"
    INAKTIV = "inaktiv"
    URLAUB = "urlaub"


class Mitarbeiter(Base):
    """Employee Model"""
    __tablename__ = "mitarbeiter"

    id = Column(Integer, primary_key=True, index=True)
    personal_nummer = Column(String(50), unique=True, nullable=False, index=True)
    vorname = Column(String(100), nullable=False)
    nachname = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    abteilung = Column(String(100), nullable=False, index=True)
    position = Column(String(100), nullable=False)
    telefon = Column(String(50), nullable=True)
    eintritt_datum = Column(Date, nullable=False)
    status = Column(SQLEnum(MitarbeiterStatus), default=MitarbeiterStatus.AKTIV, nullable=False, index=True)
    wochenstunden = Column(Numeric(5, 2), nullable=False, default=40.00)
    profilbild_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    qualifikationen = relationship(
        "MitarbeiterQualifikation",
        back_populates="mitarbeiter",
        cascade="all, delete-orphan"
    )
    verfuegbarkeiten = relationship(
        "Verfuegbarkeit",
        back_populates="mitarbeiter",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Mitarbeiter {self.personal_nummer}: {self.vorname} {self.nachname}>"

    @property
    def full_name(self):
        """Returns full name"""
        return f"{self.vorname} {self.nachname}"

    @property
    def is_available(self):
        """Check if employee is currently available"""
        return self.status == MitarbeiterStatus.AKTIV
