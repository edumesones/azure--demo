# FEAT-002: Data Storage Layer - Critical Analysis

> **Analysis Depth:** Medium (Steps 1-2-3-5-9-11)
> **Rationale:** Well-known patterns (SQLAlchemy, Alembic) but critical foundation for data persistence

---

## Step 1: Problem Clarification & Constraints

### Problem Statement
Replace the in-memory user storage with a proper database layer and establish the data model foundation for the catalog metadata (data sources, tables, columns).

### Hard Constraints
- **SQLAlchemy 2.0** - Modern async API required
- **Alembic** - Standard migration tool for SQLAlchemy
- **PostgreSQL** - Production database (JD requirement)
- **Backward Compatible** - Existing auth endpoints must keep working
- **Timeline** - 1 day for database layer

### Soft Constraints
- SQLite for development (optional but recommended)
- Repository pattern preferred for testability
- Async throughout for consistency with FastAPI

### Success Criteria
- All existing tests pass with database backend
- `alembic upgrade head` creates all tables
- User authentication works with database users
- Catalog models created (empty tables OK)
- Docker Compose includes PostgreSQL service

### Non-Goals
- Data source connection/scanning (FEAT-003+)
- Vector embeddings storage (FEAT-003)
- Complex data lineage
- Multi-tenancy

---

## Step 2: Implicit Assumptions Identification

| # | Assumption | If Wrong, Impact | Confidence | Category |
|---|------------|------------------|------------|----------|
| 1 | PostgreSQL is available in production | Need different DB | High | Environment |
| 2 | SQLite sufficient for dev/testing | May need PG locally | High | Development |
| 3 | asyncpg driver is stable | Performance issues | High | Technical |
| 4 | UUID primary keys are acceptable | Schema changes | High | Data |
| 5 | Alembic async works well | Manual migrations | Medium | Technical |
| 6 | Connection pooling defaults are OK | Tuning needed | Medium | Performance |
| 7 | Single database is sufficient | Sharding complexity | High | Architecture |

### Assumptions Requiring Validation
- Alembic async configuration - test with both SQLite and PostgreSQL

---

## Step 3: Design Space Exploration

### Approach A: Raw SQLAlchemy Core
**Core idea:** Use SQLAlchemy Core (not ORM) with raw SQL
**Pros:** Maximum control, best performance
**Cons:** More boilerplate, no relationship handling
**Best when:** High-performance, simple queries
**Effort:** Medium

### Approach B: SQLAlchemy ORM with Repository Pattern (RECOMMENDED)
**Core idea:** SQLAlchemy 2.0 ORM with repository classes
```
src/
├── db/
│   ├── base.py          # Base model class
│   ├── session.py       # Async session factory
│   └── repositories/    # CRUD operations
├── models/
│   └── db_models.py     # SQLAlchemy models
```
**Pros:**
- Clean separation of concerns
- Testable (mock repositories)
- Relationship handling
- Type hints with Mapped[]
**Cons:** Slight overhead vs raw SQL
**Best when:** Maintainable production applications
**Effort:** Medium

### Approach C: SQLModel (Pydantic + SQLAlchemy)
**Core idea:** Use SQLModel for unified Pydantic/SQLAlchemy models
**Pros:** Single model definition, less code
**Cons:** Less mature, some edge cases, mixing concerns
**Best when:** Simple CRUD applications
**Effort:** Low

### Preliminary Recommendation
**Approach B: SQLAlchemy ORM with Repository Pattern** - Industry standard, well-documented, separates concerns properly.

---

## Step 5: Failure-First Analysis

### Critical Failures (High Severity)

| Failure Mode | Probability | Severity | Detection | Mitigation |
|--------------|-------------|----------|-----------|------------|
| Database connection fails | Medium | Critical | Health check | Retry logic, clear errors |
| Migration corrupts data | Low | Critical | Backup before migrate | Test migrations, rollback plan |
| Connection pool exhaustion | Medium | High | Monitoring | Pool size config, timeouts |
| SQL injection | Low | Critical | Code review | Use ORM, never raw strings |

### Likely Failures (High Probability)

| Failure Mode | Probability | Severity | Detection | Mitigation |
|--------------|-------------|----------|-----------|------------|
| Missing DATABASE_URL | High | Medium | Startup crash | Clear error message |
| SQLite/PostgreSQL differences | High | Low | Tests on both | Abstract differences |
| Alembic migration conflicts | Medium | Medium | CI pipeline | Single migration branch |
| N+1 query problems | High | Low | Logging | Eager loading, joinedload |

### Cascading Failures
- If DB connection fails → Auth fails → All protected endpoints fail
- If migration fails → App won't start → Rollback required

---

## Step 9: Adversarial Review (Paranoid Staff Engineer Mode)

### Over-engineering Concerns
- **Don't add**: Sharding, read replicas, complex caching
- **Don't add**: Generic repository with 20 methods - just what we need
- **Don't add**: Event sourcing or CQRS patterns

### Under-engineering Concerns
- **Must have**: Proper indexes on foreign keys and email
- **Must have**: Created/updated timestamps
- **Must have**: Soft delete consideration (is_active flag)
- **Must have**: UUID primary keys (not auto-increment for distributed)

### The 2AM Incident
**Most likely:** "Database connection pool exhausted, all requests hanging"
**Prevention:**
- Configure pool_size and max_overflow properly
- Add connection timeout
- Health check includes DB connectivity

### Future Pain Points
- Migration to read replicas (acceptable - not MVP concern)
- Schema changes on large tables (use Alembic properly)

### Security Concerns
- **Connection strings**: Must be in environment, never in code
- **User passwords**: Already using bcrypt (FEAT-001)
- **SQL injection**: SQLAlchemy ORM prevents this

### Scale Concerns
- Connection pool for MVP: 5 min, 10 max
- Consider pgbouncer for production (future)

### Red Flags Found
- None critical. Standard database setup.

---

## Step 11: Decision Summary

### Recommended Approach
**SQLAlchemy 2.0 ORM with Repository Pattern**

```
src/
├── db/
│   ├── __init__.py
│   ├── base.py           # DeclarativeBase
│   ├── session.py        # async_session_maker
│   └── repositories/
│       ├── __init__.py
│       ├── base.py       # BaseRepository
│       └── user.py       # UserRepository
├── models/
│   ├── __init__.py
│   ├── schemas.py        # Pydantic (existing)
│   └── db_models.py      # SQLAlchemy models

alembic/
├── versions/
├── env.py
└── alembic.ini
```

### Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ORM | SQLAlchemy 2.0 | Modern async, type hints |
| Session | async_scoped_session | Request-scoped sessions |
| Primary keys | UUID | Distributed-friendly |
| Migrations | Alembic async | Standard tool |
| Repository | Per-model repos | Clean separation |
| Timestamps | created_at, updated_at | Audit trail |

### Short-term Goals (This Implementation)
1. Database connection and session management
2. User model + repository (replace in-memory)
3. Catalog models (DataSource, Table, Column)
4. Alembic setup with initial migration
5. Update auth to use database
6. Seed data script

### Long-term Considerations
- Connection pooling tuning for production
- Read replicas for scale
- Backup strategy

### Remaining Unknowns
- [x] All critical unknowns resolved

### Confidence Level
**High** - Standard patterns, well-documented libraries.

### Recommended Next Steps
1. Proceed to **Plan** phase
2. Create design.md with file structure
3. Create tasks.md (~15 tasks)
4. Implement

---

*Analysis completed: 2026-02-05*
*Analyst: Claude*
*Confidence: High*
*Red flags: 0 critical*
