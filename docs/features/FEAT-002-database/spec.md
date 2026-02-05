# FEAT-002: Data Storage Layer - Specification

## Overview
Set up the database infrastructure for DataCatalog AI: PostgreSQL/SQLite support, SQLAlchemy ORM with async support, Alembic migrations, and replace the in-memory user store with persistent storage.

## User Stories

### US-1: Database Connection
**As a** developer
**I want** a configured database connection with connection pooling
**So that** the application can persist data reliably

**Acceptance Criteria:**
- [ ] SQLAlchemy async engine configured
- [ ] Connection pooling with sensible defaults
- [ ] Support for PostgreSQL (production) and SQLite (development)
- [ ] Database URL from environment variable

### US-2: User Persistence
**As an** API consumer
**I want** users stored in a database
**So that** user data persists across restarts

**Acceptance Criteria:**
- [ ] User model with SQLAlchemy
- [ ] CRUD operations for users
- [ ] Migration from in-memory to database
- [ ] Seed data for test users

### US-3: Database Migrations
**As a** developer
**I want** version-controlled database migrations
**So that** schema changes are tracked and reproducible

**Acceptance Criteria:**
- [ ] Alembic configured for async SQLAlchemy
- [ ] Initial migration for users table
- [ ] Migration commands documented
- [ ] Auto-generate migration support

### US-4: Catalog Metadata Storage
**As a** data engineer
**I want** to store data catalog metadata
**So that** I can track tables, columns, and their descriptions

**Acceptance Criteria:**
- [ ] DataSource model (connection to data sources)
- [ ] Table model (metadata about tables)
- [ ] Column model (metadata about columns)
- [ ] Relationships between models

## Technical Decisions

| # | Area | Question | Decision | Notes |
|---|------|----------|----------|-------|
| 1 | ORM | Which ORM? | SQLAlchemy 2.0 | Async support, industry standard |
| 2 | Database | Production DB? | PostgreSQL | Scalable, feature-rich |
| 3 | Database | Dev DB? | SQLite | Simple, no setup needed |
| 4 | Migrations | Migration tool? | Alembic | Native SQLAlchemy support |
| 5 | Async | Async driver? | asyncpg (PG), aiosqlite (SQLite) | Best performance |

## Scope

### In Scope
- SQLAlchemy 2.0 async setup
- PostgreSQL and SQLite support
- Alembic migrations
- User model (replace in-memory)
- DataSource, Table, Column models
- CRUD repository pattern
- Database session management
- Seed data script

### Out of Scope
- Vector storage (FEAT-003)
- Full-text search
- Data source connections/scanning
- Complex query optimization

## Dependencies
- FEAT-001: Project Foundation (completed)

## Data Models

### User
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="viewer")
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow)
```

### DataSource
```python
class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(50))  # postgres, mysql, bigquery, etc.
    connection_string: Mapped[str] = mapped_column(Text)  # encrypted
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    tables: Mapped[list["Table"]] = relationship(back_populates="data_source")
```

### Table
```python
class Table(Base):
    __tablename__ = "tables"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    data_source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("data_sources.id"))
    name: Mapped[str] = mapped_column(String(255))
    schema_name: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    row_count: Mapped[int | None] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    data_source: Mapped["DataSource"] = relationship(back_populates="tables")
    columns: Mapped[list["Column"]] = relationship(back_populates="table")
```

### Column
```python
class Column(Base):
    __tablename__ = "columns"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    table_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tables.id"))
    name: Mapped[str] = mapped_column(String(255))
    data_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    is_nullable: Mapped[bool] = mapped_column(default=True)
    is_primary_key: Mapped[bool] = mapped_column(default=False)

    table: Mapped["Table"] = relationship(back_populates="columns")
```

## Security Considerations
- Connection strings encrypted at rest
- Database credentials from environment
- Parameterized queries (SQLAlchemy handles this)
- Connection pooling limits

## Performance Requirements
- Connection pool: 5-20 connections
- Query timeout: 30 seconds
- Lazy loading for relationships

---
*Created: 2026-02-05*
*Status: Draft*
