"""Pytest configuration and fixtures for DataCatalog AI tests."""

import asyncio
import os
from collections.abc import AsyncGenerator, Generator
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Set test environment variables before importing app
os.environ["JWT_SECRET_KEY"] = "test-secret-key-minimum-32-characters-long"
os.environ["DEBUG"] = "true"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_FORMAT"] = "console"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from src.api.dependencies import get_db
from src.api.main import app
from src.core.security import security_service
from src.db.base import Base
from src.db.repositories.user import UserRepository
from src.models.db_models import User
from src.models.schemas import UserInDB, UserRole

# Create test engine
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
)

test_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_maker() as session:
        yield session

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def seeded_db_session(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Database session with seeded test users."""
    user_repo = UserRepository(db_session)

    # Create test users
    await user_repo.create_user(
        email="admin@datacatalog.ai",
        password="admin123secure",
        role="admin",
    )
    await user_repo.create_user(
        email="editor@datacatalog.ai",
        password="editor123secure",
        role="editor",
    )
    await user_repo.create_user(
        email="viewer@datacatalog.ai",
        password="viewer123secure",
        role="viewer",
    )

    await db_session.commit()
    yield db_session


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override get_db dependency for testing."""
    async with test_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
def test_client(seeded_db_session: AsyncSession) -> Generator[TestClient, None, None]:
    """Create a test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def async_client(seeded_db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
    app.dependency_overrides.clear()


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
def admin_access_token() -> str:
    """Generate a valid admin access token for testing with seeded user."""
    return security_service.create_access_token(
        data={
            "sub": "admin-uuid",
            "email": "admin@datacatalog.ai",
            "role": "admin",
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
