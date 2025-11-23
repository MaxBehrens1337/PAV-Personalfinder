"""
Authentication Service
Handles user authentication, password hashing, and JWT token generation
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.database import get_db
from app.models.user import User, UserRolle
from app.schemas.user import TokenData


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class AuthService:
    """Service for authentication and authorization"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token

        Args:
            data: Data to encode in token
            expires_delta: Token expiration time

        Returns:
            JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user

        Args:
            db: Database session
            username: Username
            password: Password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return None

        if not auth_service.verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        # Update last login
        user.last_login_at = datetime.utcnow()
        db.commit()

        return user

    @staticmethod
    def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
        """
        Get current authenticated user from JWT token

        Args:
            token: JWT token
            db: Database session

        Returns:
            User object

        Raises:
            HTTPException: If token is invalid or user not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")

            if username is None or user_id is None:
                raise credentials_exception

            token_data = TokenData(username=username, user_id=user_id)

        except JWTError:
            raise credentials_exception

        user = db.query(User).filter(User.id == token_data.user_id).first()

        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        return user

    @staticmethod
    def get_current_active_user(
        current_user: User = Depends(get_current_user)
    ) -> User:
        """
        Get current active user (alias for get_current_user)

        Args:
            current_user: Current user from get_current_user dependency

        Returns:
            User object
        """
        return current_user

    @staticmethod
    def require_role(allowed_roles: list[UserRolle]):
        """
        Dependency to require specific user roles

        Args:
            allowed_roles: List of allowed roles

        Returns:
            Dependency function

        Example:
            @app.get("/admin", dependencies=[Depends(require_role([UserRolle.ADMIN]))])
        """
        def role_checker(current_user: User = Depends(auth_service.get_current_user)):
            if current_user.rolle not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
                )
            return current_user

        return role_checker

    @staticmethod
    def can_write(current_user: User = Depends(get_current_user)) -> User:
        """
        Dependency to check if user can write/modify data

        Args:
            current_user: Current user

        Returns:
            User object

        Raises:
            HTTPException: If user doesn't have write permission
        """
        if current_user.rolle == UserRolle.READONLY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Read-only users cannot modify data"
            )
        return current_user

    @staticmethod
    def is_admin(current_user: User = Depends(get_current_user)) -> User:
        """
        Dependency to check if user is admin

        Args:
            current_user: Current user

        Returns:
            User object

        Raises:
            HTTPException: If user is not admin
        """
        if current_user.rolle != UserRolle.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user


# Global instance
auth_service = AuthService()
