"""Authentication router for login, token refresh, and user info."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import settings
from src.core.exceptions import (
    credentials_exception,
    invalid_credentials_exception,
    token_expired_exception,
)
from src.core.security import security_service
from src.models.schemas import (
    LoginResponse,
    Token,
    TokenRefresh,
    User,
    UserInDB,
    UserRole,
)

router = APIRouter(prefix="/auth", tags=["authentication"])

# In-memory user store for MVP (will be replaced with database in FEAT-002)
FAKE_USERS_DB: dict[str, UserInDB] = {
    "admin@datacatalog.ai": UserInDB(
        id="user-001",
        email="admin@datacatalog.ai",
        full_name="Admin User",
        is_active=True,
        role=UserRole.ADMIN,
        hashed_password=security_service.hash_password("admin123secure"),
        created_at=datetime.now(timezone.utc),
    ),
    "editor@datacatalog.ai": UserInDB(
        id="user-002",
        email="editor@datacatalog.ai",
        full_name="Editor User",
        is_active=True,
        role=UserRole.EDITOR,
        hashed_password=security_service.hash_password("editor123secure"),
        created_at=datetime.now(timezone.utc),
    ),
    "viewer@datacatalog.ai": UserInDB(
        id="user-003",
        email="viewer@datacatalog.ai",
        full_name="Viewer User",
        is_active=True,
        role=UserRole.VIEWER,
        hashed_password=security_service.hash_password("viewer123secure"),
        created_at=datetime.now(timezone.utc),
    ),
}


def get_user_by_email(email: str) -> UserInDB | None:
    """Get user from fake database by email."""
    return FAKE_USERS_DB.get(email)


def authenticate_user(email: str, password: str) -> UserInDB | None:
    """Authenticate user with email and password."""
    user = get_user_by_email(email)
    if not user:
        return None
    if not security_service.verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login endpoint.

    Returns access and refresh tokens for valid credentials.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise invalid_credentials_exception()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    access_token = security_service.create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )
    refresh_token = security_service.create_refresh_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(token_data: TokenRefresh) -> Token:
    """
    Refresh access token using refresh token.

    Returns new access and refresh tokens.
    """
    try:
        payload = security_service.verify_token(token_data.refresh_token, "refresh")
    except Exception:
        raise credentials_exception()

    user_email = payload.get("email")
    user = get_user_by_email(user_email)

    if not user:
        raise credentials_exception()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    access_token = security_service.create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )
    refresh_token = security_service.create_refresh_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: Annotated["User", Depends("get_current_user")],
) -> User:
    """
    Get current authenticated user information.

    Requires valid access token in Authorization header.
    """
    # This endpoint uses the get_current_user dependency from dependencies.py
    # The import is done in main.py to avoid circular imports
    return current_user
