"""FastAPI dependencies for dependency injection."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
    credentials_exception,
    forbidden_exception,
    token_expired_exception,
)
from src.core.security import security_service
from src.models.schemas import User, UserInDB, UserRole

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# In-memory user store (shared with auth router - will be replaced with DB)
# This is duplicated here for MVP; will be refactored in FEAT-002 with proper DB
FAKE_USERS_DB: dict[str, UserInDB] = {}


def _init_fake_db() -> None:
    """Initialize fake database - called from auth router."""
    from src.api.routers.auth import FAKE_USERS_DB as AUTH_USERS_DB

    global FAKE_USERS_DB
    FAKE_USERS_DB = AUTH_USERS_DB


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    Args:
        token: JWT access token from Authorization header

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

    # Initialize fake DB if needed
    if not FAKE_USERS_DB:
        _init_fake_db()

    user = FAKE_USERS_DB.get(user_email)
    if user is None:
        raise credentials_exception()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    # Return User without hashed_password
    return User(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
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
