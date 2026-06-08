# DataCatalog AI

Intelligent data catalog with **RAG-powered natural-language querying**, built as a
**production-shaped FastAPI service**: JWT auth, async SQL persistence, database
migrations, structured logging and Prometheus metrics out of the box.

## What it demonstrates (production API patterns)

- **Async FastAPI** with SQLAlchemy 2.0 (async) + asyncpg/aiosqlite and **Alembic
  migrations** — not a toy script, a service with a real data layer.
- **Auth**: OAuth2 password flow with JWT access/refresh tokens
  (`python-jose`, `passlib`/bcrypt).
- **Observability**: `structlog` structured logging + **Prometheus** `/metrics`,
  plus `/health` and `/ready` probes for orchestration.
- **RAG over the catalog**: query datasets/metadata in natural language.
- Built with a **spec-driven methodology** — the `.claude/` folder ships the skills and
  commands (spec-architect, architecture-designer, implementation-planner, …) used to
  design and implement it with traceability from spec to code.

## API surface
```
GET  /api/v1/health | /ready | /metrics       health & Prometheus
POST /api/v1/auth/token | /auth/refresh        OAuth2 login / refresh
GET  /api/v1/auth/me                           current user
GET  /api/docs                                 OpenAPI docs
```

## Tech stack
Python 3.11 · FastAPI · Pydantic v2 · SQLAlchemy (async) · asyncpg / aiosqlite ·
Alembic · python-jose + passlib · structlog · prometheus-client · Docker Compose

## Quick start
```bash
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"
cp .env.example .env
uvicorn src.api.main:app --reload      # http://localhost:8000/api/docs
# or: cd docker && docker-compose up -d
```
