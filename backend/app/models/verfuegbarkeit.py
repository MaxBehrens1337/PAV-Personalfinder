"""
Verfuegbarkeit Model
Employee availability model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class VerfuegbarkeitTyp(str, enum.Enum):
    """Availability type enum"""
    URLAUB = "urlaub"
    KRANK = "krank"
    EINSATZ = "einsatz"
    VERFUEGBAR = "verfuegbar"
    SONSTIGES = "sonstiges"


class Verfuegbarkeit(Base):
    """Employee Availability Model"""
    __tablename__ = "verfuegbarkeit"

    id = Column(Integer, primary_key=True, index=True)
    mitarbeiter_id = Column(Integer, ForeignKey("mitarbeiter.id", ondelete="CASCADE"), nullable=False, index=True)
    typ = Column(SQLEnum(VerfuegbarkeitTyp), nullable=False, index=True)
    von_datum = Column(Date, nullable=False, index=True)
    bis_datum = Column(Date, nullable=False, index=True)
    notizen = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    mitarbeiter = relationship("Mitarbeiter", back_populates="verfuegbarkeiten")

    def __repr__(self):
        return f"<Verfuegbarkeit MA:{self.mitarbeiter_id} {self.typ} {self.von_datum}-{self.bis_datum}>"

    @property
    def is_current(self):
        """Check if availability period includes today"""
        from datetime import date
        today = date.today()
        return self.von_datum <= today <= self.bis_datum

    @property
    def is_future(self):
        """Check if availability is in the future"""
        from datetime import date
        return self.von_datum > date.today()

    @property
    def is_past(self):
        """Check if availability is in the past"""
        from datetime import date
        return self.bis_datum < date.today()

    @property
    def duration_days(self):
        """Calculate duration in days"""
        return (self.bis_datum - self.von_datum).days + 1
