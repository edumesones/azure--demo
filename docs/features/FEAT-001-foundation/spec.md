# FEAT-001: Project Foundation - Specification

## Overview
Set up the foundational infrastructure for DataCatalog AI: project scaffolding, configuration management, Docker setup, authentication system (JWT/OAuth2), health endpoints, and essential middleware.

## User Stories

### US-1: Project Setup
**As a** developer
**I want** a well-structured Python project with proper configuration
**So that** I can start building features efficiently

**Acceptance Criteria:**
- [x] Project follows standard Python package structure
- [x] pyproject.toml with all dependencies
- [x] Environment-based configuration (Pydantic Settings)
- [x] .env.example with all required variables

### US-2: Docker Development Environment
**As a** developer
**I want** a Docker Compose setup for local development
**So that** I can run the entire stack with one command

**Acceptance Criteria:**
- [x] Dockerfile with multi-stage build
- [x] docker-compose.yml with API service
- [x] Hot-reload in development mode
- [x] Health check configured

### US-3: Authentication
**As an** API consumer
**I want** JWT-based authentication
**So that** I can securely access protected endpoints

**Acceptance Criteria:**
- [x] POST /auth/token - Get JWT token
- [x] POST /auth/refresh - Refresh token
- [x] JWT with 24h expiry, refresh with 7d expiry
- [x] RBAC with viewer/editor/admin roles

### US-4: Health & Monitoring
**As an** operator
**I want** health and metrics endpoints
**So that** I can monitor the API status

**Acceptance Criteria:**
- [x] GET /health - Basic health check
- [x] GET /metrics - Prometheus-compatible metrics
- [x] Structured JSON logging with correlation IDs

## Technical Decisions

| # | Area | Question | Decision | Notes |
|---|------|----------|----------|-------|
| 1 | Framework | API framework | FastAPI | Async, auto-docs |
| 2 | Config | Configuration management | Pydantic Settings | Type-safe, env-based |
| 3 | Auth | Token format | JWT (python-jose) | Stateless, OAuth2 compatible |
| 4 | Logging | Log format | JSON structured | With correlation IDs |
| 5 | Container | Base image | python:3.11-slim | Balance size/compatibility |

## Scope

### In Scope
- FastAPI application factory pattern
- Pydantic Settings configuration
- JWT authentication with RBAC
- Health and metrics endpoints
- CORS middleware
- Rate limiting middleware
- Structured logging with correlation IDs
- Dockerfile + docker-compose.yml
- Basic pytest setup

### Out of Scope
- Business logic endpoints (next features)
- Database setup (next feature)
- Vector store setup (FEAT-003)
- Demo data (FEAT-005)

## Dependencies
- None (this is the foundation)

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /auth/token | Get JWT access token | No |
| POST | /auth/refresh | Refresh access token | Yes (refresh token) |
| GET | /auth/me | Get current user info | Yes |
| GET | /health | Basic health check | No |
| GET | /metrics | Prometheus metrics | No |

## Data Models

### User (in-memory for MVP)
```python
class User(BaseModel):
    id: str
    email: str
    role: Literal["viewer", "editor", "admin"]
    is_active: bool = True
```

### Token Response
```python
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
```

## Security Considerations
- JWT secret from environment variable
- Password hashing with bcrypt (passlib)
- Token expiry: access=24h, refresh=7d
- HTTPS only in production
- CORS configured for allowed origins

## Performance Requirements
- Health endpoint < 50ms
- Token generation < 100ms
- Startup time < 5 seconds

---
*Created: 2026-02-05*
*Status: Ready for Think Critically phase*
