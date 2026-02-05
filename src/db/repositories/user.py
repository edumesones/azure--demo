"""User repository for authentication operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import security_service
from src.db.repositories.base import BaseRepository
from src.models.db_models import User


class UserRepository(BaseRepository[User]):
    """Repository for User model with authentication methods."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize user repository."""
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email address.

        Args:
            email: User email address

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> User | None:
        """
        Authenticate user with email and password.

        Args:
            email: User email address
            password: Plain text password

        Returns:
            User if authentication successful, None otherwise
        """
        user = await self.get_by_email(email)
        if user is None:
            return None

        if not user.is_active:
            return None

        if not security_service.verify_password(password, user.hashed_password):
            return None

        return user

    async def create_user(
        self,
        email: str,
        password: str,
        role: str = "viewer",
        is_active: bool = True,
    ) -> User:
        """
        Create new user with hashed password.

        Args:
            email: User email address
            password: Plain text password (will be hashed)
            role: User role (viewer, editor, admin)
            is_active: Whether user is active

        Returns:
            Created user
        """
        hashed_password = security_service.hash_password(password)
        return await self.create(
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_active=is_active,
        )

    async def update_password(self, user_id, new_password: str) -> User | None:
        """
        Update user password.

        Args:
            user_id: User UUID
            new_password: New plain text password (will be hashed)

        Returns:
            Updated user if found, None otherwise
        """
        hashed_password = security_service.hash_password(new_password)
        return await self.update(user_id, hashed_password=hashed_password)

    async def get_active_users(self) -> list[User]:
        """
        Get all active users.

        Returns:
            List of active users
        """
        stmt = select(User).where(User.is_active == True)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
