"""Pytest configuration and fixtures for DataCatalog AI tests."""

import os
from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["JWT_SECRET_KEY"] = "test-secret-key-minimum-32-characters-long"
os.environ["DEBUG"] = "true"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_FORMAT"] = "console"

from src.api.main import app
from src.core.security import security_service
from src.models.schemas import UserInDB, UserRole


@pytest.fixture(scope="session")
def test_client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user() -> UserInDB:
    """Create a test user for authentication tests."""
    return UserInDB(
        id="test-user-001",
        email="test@datacatalog.ai",
        full_name="Test User",
        is_active=True,
        role=UserRole.EDITOR,
        hashed_password=security_service.hash_password("testpassword123"),
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def test_admin_user() -> UserInDB:
    """Create a test admin user."""
    return UserInDB(
        id="test-admin-001",
        email="admin@datacatalog.ai",
        full_name="Admin User",
        is_active=True,
        role=UserRole.ADMIN,
        hashed_password=security_service.hash_password("adminpassword123"),
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def access_token(test_user: UserInDB) -> str:
    """Generate a valid access token for testing."""
    return security_service.create_access_token(
        data={
            "sub": test_user.id,
            "email": test_user.email,
            "role": test_user.role.value,
        }
    )


@pytest.fixture
def admin_access_token(test_admin_user: UserInDB) -> str:
    """Generate a valid admin access token for testing."""
    return security_service.create_access_token(
        data={
            "sub": test_admin_user.id,
            "email": test_admin_user.email,
            "role": test_admin_user.role.value,
        }
    )


@pytest.fixture
def auth_headers(access_token: str) -> dict[str, str]:
    """Generate authorization headers with access token."""
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def admin_auth_headers(admin_access_token: str) -> dict[str, str]:
    """Generate authorization headers with admin access token."""
    return {"Authorization": f"Bearer {admin_access_token}"}
