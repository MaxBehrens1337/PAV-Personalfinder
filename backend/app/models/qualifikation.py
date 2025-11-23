"""
Qualifikation Models
Qualification and employee-qualification association models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class QualifikationKategorie(str, enum.Enum):
    """Qualification category enum"""
    ZERTIFIKAT = "zertifikat"
    SKILL = "skill"
    ERFAHRUNG = "erfahrung"


class QualifikationLevel(str, enum.Enum):
    """Skill level enum"""
    ANFAENGER = "anfaenger"
    FORTGESCHRITTEN = "fortgeschritten"
    EXPERTE = "experte"


class Qualifikation(Base):
    """Qualification Master Model"""
    __tablename__ = "qualifikationen"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    kategorie = Column(SQLEnum(QualifikationKategorie), nullable=False, index=True)
    beschreibung = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    mitarbeiter_qualifikationen = relationship(
        "MitarbeiterQualifikation",
        back_populates="qualifikation",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Qualifikation {self.name} ({self.kategorie})>"


class MitarbeiterQualifikation(Base):
    """Employee-Qualification Association Model (Many-to-Many with extra fields)"""
    __tablename__ = "mitarbeiter_qualifikationen"

    id = Column(Integer, primary_key=True, index=True)
    mitarbeiter_id = Column(Integer, ForeignKey("mitarbeiter.id", ondelete="CASCADE"), nullable=False, index=True)
    qualifikation_id = Column(Integer, ForeignKey("qualifikationen.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(SQLEnum(QualifikationLevel), default=QualifikationLevel.FORTGESCHRITTEN, nullable=False)
    gueltig_von = Column(Date, nullable=True)
    gueltig_bis = Column(Date, nullable=True)
    notizen = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    mitarbeiter = relationship("Mitarbeiter", back_populates="qualifikationen")
    qualifikation = relationship("Qualifikation", back_populates="mitarbeiter_qualifikationen")

    def __repr__(self):
        return f"<MitarbeiterQualifikation MA:{self.mitarbeiter_id} Q:{self.qualifikation_id} ({self.level})>"

    @property
    def is_valid(self):
        """Check if qualification is currently valid"""
        from datetime import date
        today = date.today()

        if self.gueltig_bis is None:
            return True

        return self.gueltig_bis >= today

    @property
    def is_expiring_soon(self, days=30):
        """Check if qualification is expiring within specified days"""
        from datetime import date, timedelta

        if self.gueltig_bis is None:
            return False

        threshold = date.today() + timedelta(days=days)
        return self.gueltig_bis <= threshold and self.gueltig_bis >= date.today()
