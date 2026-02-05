"""Pydantic schemas for API request/response models."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User roles for RBAC."""

    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"


class TokenType(str, Enum):
    """Token types."""

    ACCESS = "access"
    REFRESH = "refresh"


# User schemas
class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.VIEWER


class User(UserBase):
    """User schema for responses."""

    id: str
    role: UserRole
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class UserInDB(User):
    """User schema with hashed password (internal use)."""

    hashed_password: str


class UserResponse(BaseModel):
    """API response for user data."""

    user: User
    message: str = "Success"


# Token schemas
class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenPayload(BaseModel):
    """JWT token payload schema."""

    sub: str  # User ID
    email: str
    role: UserRole
    type: TokenType
    exp: datetime
    iat: datetime


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""

    refresh_token: str


# Auth schemas
class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


# Health check schemas
class HealthStatus(str, Enum):
    """Health check status values."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheck(BaseModel):
    """Health check response schema."""

    status: HealthStatus
    version: str
    timestamp: datetime


class ReadinessCheck(BaseModel):
    """Readiness check response schema."""

    status: HealthStatus
    checks: dict[str, bool] = Field(default_factory=dict)
    timestamp: datetime
