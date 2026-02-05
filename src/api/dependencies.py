"""FastAPI dependencies for dependency injection."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
    credentials_exception,
    forbidden_exception,
    token_expired_exception,
)
from src.core.security import security_service
from src.db.repositories.user import UserRepository
from src.db.session import async_session_maker
from src.models.schemas import User, UserInDB, UserRole

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.

    Yields:
        AsyncSession: Database session that auto-commits on success
        and rolls back on exception.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    Args:
        token: JWT access token from Authorization header
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        payload = security_service.verify_token(token, "access")
    except TokenExpiredError:
        raise token_expired_exception()
    except InvalidTokenError:
        raise credentials_exception()

    user_email = payload.get("email")
    if user_email is None:
        raise credentials_exception()

    # Get user from database
    user_repo = UserRepository(db)
    db_user = await user_repo.get_by_email(user_email)

    if db_user is None:
        raise credentials_exception()

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    # Return User schema
    return User(
        id=str(db_user.id),
        email=db_user.email,
        full_name=None,  # Not in DB model yet
        is_active=db_user.is_active,
        role=UserRole(db_user.role),
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Dependency to ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


def require_role(required_roles: list[UserRole]):
    """
    Dependency factory for role-based access control.

    Args:
        required_roles: List of roles that are allowed to access the endpoint

    Returns:
        Dependency function that validates user role
    """

    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if current_user.role not in required_roles:
            raise forbidden_exception(
                f"This action requires one of the following roles: {[r.value for r in required_roles]}"
            )
        return current_user

    return role_checker


# Pre-built role dependencies for common use cases
require_admin = require_role([UserRole.ADMIN])
require_editor = require_role([UserRole.ADMIN, UserRole.EDITOR])
require_viewer = require_role([UserRole.ADMIN, UserRole.EDITOR, UserRole.VIEWER])
