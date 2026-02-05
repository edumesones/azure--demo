# FEAT-002: Data Storage Layer - Technical Design

## Overview
SQLAlchemy 2.0 async database layer with Alembic migrations, replacing in-memory user storage and establishing catalog metadata models.

## Architecture

### System Context
```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                     API Layer                          │ │
│  │  /auth/*  │  /health  │  /api/v1/catalog/*            │ │
│  └─────────────────────┬──────────────────────────────────┘ │
│                        │                                    │
│  ┌─────────────────────▼──────────────────────────────────┐ │
│  │                  Dependencies                          │ │
│  │  get_db_session()  │  get_current_user()              │ │
│  └─────────────────────┬──────────────────────────────────┘ │
│                        │                                    │
│  ┌─────────────────────▼──────────────────────────────────┐ │
│  │                  Repositories                          │ │
│  │  UserRepository  │  DataSourceRepo  │  TableRepo      │ │
│  └─────────────────────┬──────────────────────────────────┘ │
│                        │                                    │
│  ┌─────────────────────▼──────────────────────────────────┐ │
│  │               SQLAlchemy Session                       │ │
│  │  AsyncSession  │  Connection Pool                     │ │
│  └─────────────────────┬──────────────────────────────────┘ │
└────────────────────────┼────────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │     PostgreSQL      │
              │  (or SQLite dev)    │
              └─────────────────────┘
```

### Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| Base Model | SQLAlchemy declarative base | `src/db/base.py` |
| Session Factory | Async session creation | `src/db/session.py` |
| DB Models | SQLAlchemy ORM models | `src/models/db_models.py` |
| Repositories | CRUD operations | `src/db/repositories/` |
| Alembic | Database migrations | `alembic/` |
| Seed Script | Initial data | `scripts/seed.py` |

## Database Schema

### ERD
```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK, UUID)   │
│ email (UNIQUE)  │
│ hashed_password │
│ role            │
│ is_active       │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  data_sources   │       │     tables      │       │    columns      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK, UUID)   │──┐    │ id (PK, UUID)   │──┐    │ id (PK, UUID)   │
│ name (UNIQUE)   │  │    │ data_source_id  │◄─┘    │ table_id (FK)   │◄─┘
│ description     │  │    │ name            │       │ name            │
│ source_type     │  └───►│ schema_name     │       │ data_type       │
│ connection_str  │       │ description     │       │ description     │
│ is_active       │       │ row_count       │       │ is_nullable     │
│ created_at      │       │ created_at      │       │ is_primary_key  │
│ updated_at      │       │ updated_at      │       │ created_at      │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

## File Structure

### New Files
```
src/
├── db/
│   ├── __init__.py
│   ├── base.py              # DeclarativeBase, metadata
│   ├── session.py           # async engine, session factory
│   └── repositories/
│       ├── __init__.py
│       ├── base.py          # BaseRepository[T]
│       ├── user.py          # UserRepository
│       ├── data_source.py   # DataSourceRepository
│       └── catalog.py       # TableRepository, ColumnRepository
├── models/
│   └── db_models.py         # User, DataSource, Table, Column

alembic/
├── alembic.ini
├── env.py                   # Async alembic config
├── script.py.mako
└── versions/
    └── 001_initial.py       # Initial migration

scripts/
└── seed.py                  # Seed data script

docker/
└── docker-compose.yml       # Add PostgreSQL service
```

### Modified Files
```
src/core/config.py           # Add DATABASE_URL
src/api/dependencies.py      # Add get_db dependency
src/api/routers/auth.py      # Use UserRepository
src/api/routers/health.py    # Add DB health check
.env.example                 # Add DATABASE_URL
pyproject.toml               # Add sqlalchemy, alembic deps
```

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/datacatalog
# Or for development
DATABASE_URL=sqlite+aiosqlite:///./data/app.db

# Pool settings (optional)
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
```

## Implementation Details

### Session Management
```python
# src/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Repository Pattern
```python
# src/db/repositories/base.py
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance
```

## Migration Strategy

### Alembic Commands
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Implementation Order
1. Add database dependencies to pyproject.toml
2. Create src/db/base.py (DeclarativeBase)
3. Create src/db/session.py (engine, session factory)
4. Create src/models/db_models.py (User, DataSource, Table, Column)
5. Create src/db/repositories/ (base, user, catalog)
6. Configure Alembic
7. Create initial migration
8. Update config.py with DATABASE_URL
9. Update dependencies.py with get_db
10. Update auth.py to use UserRepository
11. Update health.py with DB check
12. Update docker-compose.yml with PostgreSQL
13. Create seed.py script
14. Update tests
15. Update .env.example

---
*Generated: 2026-02-05*
*Status: Ready for implementation*
