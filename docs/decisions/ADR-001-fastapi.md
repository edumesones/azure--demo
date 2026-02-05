# ADR-001: Use FastAPI for Backend Framework

## Status
Accepted

## Date
2026-02-05

## Context
We need a Python backend framework for DataCatalog AI. Requirements:
- REST API endpoints with auto-generated docs
- Native async support for non-blocking I/O
- High performance for concurrent requests
- Pydantic validation built-in
- JD requirement alignment

## Options Considered

### Option 1: FastAPI
**Pros:**
- Native async support (critical for LLM/embedding API calls)
- Automatic OpenAPI/Swagger documentation
- Pydantic v2 validation built-in
- High performance (one of fastest Python frameworks)
- Modern Python typing support

**Cons:**
- Smaller ecosystem than Django
- Less batteries-included

### Option 2: Django + DRF
**Pros:**
- Batteries included (admin, ORM, auth)
- Large ecosystem, mature

**Cons:**
- Sync by default (async is bolted on)
- Heavier for API-only projects
- Slower than FastAPI

### Option 3: Flask
**Pros:**
- Simple and flexible
- Large ecosystem

**Cons:**
- No built-in validation
- Manual OpenAPI setup
- Sync only without extensions

## Decision
**FastAPI** - Best fit for async API with auto-documentation needs. Critical for non-blocking LLM and embedding API calls.

## Consequences
- All endpoints will be `async def`
- Use Pydantic v2 for all request/response models
- SQLAlchemy with async driver for database operations
- Team needs FastAPI familiarity (minimal learning curve for Python devs)

## References
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Benchmark comparisons](https://www.techempower.com/benchmarks/)
