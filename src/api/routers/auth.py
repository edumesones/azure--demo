"""Authentication router for login, token refresh, and user info."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user, get_db
from src.core.config import settings
from src.core.exceptions import (
    credentials_exception,
    invalid_credentials_exception,
)
from src.core.security import security_service
from src.db.repositories.user import UserRepository
from src.models.schemas import (
    Token,
    TokenRefresh,
    User,
    UserRole,
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """
    OAuth2 compatible token login endpoint.

    Returns access and refresh tokens for valid credentials.
    """
    user_repo = UserRepository(db)
    user = await user_repo.authenticate(form_data.username, form_data.password)

    if not user:
        raise invalid_credentials_exception()

    access_token = security_service.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = security_service.create_refresh_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    token_data: TokenRefresh,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """
    Refresh access token using refresh token.

    Returns new access and refresh tokens.
    """
    try:
        payload = security_service.verify_token(token_data.refresh_token, "refresh")
    except Exception:
        raise credentials_exception()

    user_email = payload.get("email")
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(user_email)

    if not user:
        raise credentials_exception()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    access_token = security_service.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = security_service.create_refresh_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Get current authenticated user information.

    Requires valid access token in Authorization header.
    """
    return current_user
