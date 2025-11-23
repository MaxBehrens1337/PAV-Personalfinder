"""
User Model
System user model for authentication and authorization
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class UserRolle(str, enum.Enum):
    """User role enum"""
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"


class User(Base):
    """System User Model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rolle = Column(SQLEnum(UserRolle), default=UserRolle.USER, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    suchanfragen = relationship("Suchanfrage", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} ({self.rolle})>"

    @property
    def is_admin(self):
        """Check if user has admin role"""
        return self.rolle == UserRolle.ADMIN

    @property
    def can_write(self):
        """Check if user can write/modify data"""
        return self.rolle in [UserRolle.ADMIN, UserRolle.USER]

    @property
    def can_read_only(self):
        """Check if user is read-only"""
        return self.rolle == UserRolle.READONLY
