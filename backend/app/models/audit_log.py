"""
AuditLog Model
Audit trail for compliance and DSGVO
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class AuditAction(str, enum.Enum):
    """Audit action types"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SEARCH = "search"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"


class AuditLog(Base):
    """Audit Log Model for tracking all critical actions"""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    entity_type = Column(String(100), nullable=True, index=True)  # e.g., "mitarbeiter", "qualifikation"
    entity_id = Column(Integer, nullable=True)
    changes = Column(JSON, nullable=True)  # Store what was changed
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 ready
    user_agent = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.entity_type}:{self.entity_id} by User:{self.user_id}>"

    @classmethod
    def log_action(cls, db, user_id, action, entity_type=None, entity_id=None, changes=None, ip_address=None, user_agent=None):
        """
        Helper method to create audit log entry

        Args:
            db: Database session
            user_id: User ID performing the action
            action: AuditAction enum value
            entity_type: Type of entity (optional)
            entity_id: ID of entity (optional)
            changes: Dict of changes (optional)
            ip_address: Client IP address (optional)
            user_agent: Client user agent (optional)

        Returns:
            AuditLog instance
        """
        log = cls(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log)
        db.commit()
        return log
