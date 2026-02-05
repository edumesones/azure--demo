#!/usr/bin/env python3
"""Seed script to populate database with initial data."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config import settings
from src.db.repositories.user import UserRepository
from src.db.session import async_session_maker, engine
from src.models.db_models import Base


async def create_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")


async def seed_users() -> None:
    """Seed initial users."""
    users_data = [
        {
            "email": "admin@datacatalog.ai",
            "password": "admin123secure",
            "role": "admin",
        },
        {
            "email": "editor@datacatalog.ai",
            "password": "editor123secure",
            "role": "editor",
        },
        {
            "email": "viewer@datacatalog.ai",
            "password": "viewer123secure",
            "role": "viewer",
        },
    ]

    async with async_session_maker() as session:
        user_repo = UserRepository(session)

        for user_data in users_data:
            existing = await user_repo.get_by_email(user_data["email"])
            if existing:
                print(f"  User {user_data['email']} already exists, skipping.")
                continue

            user = await user_repo.create_user(
                email=user_data["email"],
                password=user_data["password"],
                role=user_data["role"],
            )
            print(f"  Created user: {user.email} (role: {user.role})")

        await session.commit()

    print("Users seeded successfully.")


async def main() -> None:
    """Main seed function."""
    print(f"Seeding database: {settings.database_url}")
    print("-" * 50)

    # Create tables
    await create_tables()

    # Seed users
    print("\nSeeding users...")
    await seed_users()

    print("\n" + "=" * 50)
    print("Database seeding complete!")
    print("=" * 50)

    # Close engine
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
