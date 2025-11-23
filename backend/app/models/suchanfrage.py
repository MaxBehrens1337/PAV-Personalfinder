"""
Suchanfrage Model
Saved search queries model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Suchanfrage(Base):
    """Saved Search Query Model"""
    __tablename__ = "suchanfragen"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    query_text = Column(Text, nullable=False)
    filter_params = Column(JSON, nullable=True)  # Store filter parameters as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    use_count = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="suchanfragen")

    def __repr__(self):
        return f"<Suchanfrage '{self.name}' by User:{self.user_id}>"

    def increment_usage(self):
        """Increment usage counter and update last used timestamp"""
        from datetime import datetime
        self.use_count += 1
        self.last_used_at = datetime.now()
