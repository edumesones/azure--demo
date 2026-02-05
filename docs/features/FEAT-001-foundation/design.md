# FEAT-001: Project Foundation - Technical Design

## Overview
FastAPI application with Application Factory pattern, JWT authentication, health endpoints, and Docker setup for DataCatalog AI.

## Architecture

### System Context
```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                           │
│  Swagger UI / curl / Tests                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP + JWT
┌──────────────────────▼──────────────────────────────────────┐
│                   FastAPI Application                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Middleware                         │   │
│  │  CORS │ Rate Limit (stub) │ Logging │ Correlation ID │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │
│  │ /auth/*    │  │ /health    │  │ /metrics           │    │
│  │ Router     │  │ Router     │  │ Router             │    │
│  └─────┬──────┘  └────────────┘  └────────────────────┘    │
│        │                                                    │
│  ┌─────▼──────┐                                            │
│  │ Security   │                                            │
│  │ Service    │                                            │
│  │ (JWT)      │                                            │
│  └────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| App Factory | Create FastAPI app | `src/api/main.py` |
| Config | Environment settings | `src/core/config.py` |
| Security | JWT encode/decode | `src/core/security.py` |
| Auth Router | Login/refresh/me | `src/api/routers/auth.py` |
| Health Router | Health/metrics | `src/api/routers/health.py` |
| Middleware | CORS, logging | `src/api/middleware.py` |
| Dependencies | DI utilities | `src/api/dependencies.py` |

## Data Model

### User (In-Memory)
```python
class User(BaseModel):
    id: str
    email: str
    hashed_password: str
    role: Literal["viewer", "editor", "admin"]
    is_active: bool = True

# In-memory store with 3 test users
USERS_DB: dict[str, User] = {
    "admin@example.com": User(id="1", email="admin@example.com", hashed_password="...", role="admin"),
    "editor@example.com": User(id="2", email="editor@example.com", hashed_password="...", role="editor"),
    "viewer@example.com": User(id="3", email="viewer@example.com", hashed_password="...", role="viewer"),
}
```

### Token Schemas
```python
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str  # user email
    role: str
    exp: datetime
    type: Literal["access", "refresh"]
```

## API Design

### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /auth/token | Get JWT tokens | No |
| POST | /auth/refresh | Refresh access token | Yes (refresh) |
| GET | /auth/me | Get current user | Yes |
| GET | /health | Health check | No |
| GET | /health/ready | Readiness check | No |
| GET | /metrics | Prometheus metrics | No |

### Examples

**POST /auth/token**
```json
// Request (form-data)
{
  "username": "admin@example.com",
  "password": "admin123"
}

// Response
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**GET /auth/me**
```json
// Response
{
  "id": "1",
  "email": "admin@example.com",
  "role": "admin",
  "is_active": true
}
```

**GET /health**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T10:30:00Z",
  "version": "0.1.0"
}
```

## Service Layer

| Service | Methods | Dependencies |
|---------|---------|--------------|
| SecurityService | create_access_token, create_refresh_token, verify_token, verify_password, hash_password | python-jose, passlib |

## Error Handling

| Error Case | HTTP Code | Response |
|------------|-----------|----------|
| Invalid credentials | 401 | `{"detail": "Invalid credentials"}` |
| Token expired | 401 | `{"detail": "Token expired"}` |
| Invalid token | 401 | `{"detail": "Could not validate credentials"}` |
| Insufficient permissions | 403 | `{"detail": "Insufficient permissions"}` |
| Validation error | 422 | Pydantic validation errors |

## Security Considerations
- JWT_SECRET from env var (min 32 chars, fail if missing)
- bcrypt password hashing (passlib)
- Token expiry: access=24h, refresh=7d
- Constant-time password comparison

## File Structure

### New Files
```
src/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── main.py              # create_app() factory
│   ├── dependencies.py      # get_current_user, etc.
│   ├── middleware.py        # CORS, logging middleware
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # /auth/* endpoints
│       └── health.py        # /health, /metrics
├── core/
│   ├── __init__.py
│   ├── config.py            # Settings class
│   ├── security.py          # JWT utilities
│   └── exceptions.py        # Custom exceptions
└── models/
    ├── __init__.py
    └── schemas.py           # Pydantic models

tests/
├── __init__.py
├── conftest.py              # Fixtures
└── test_auth.py             # Auth endpoint tests

docker/
├── Dockerfile
└── docker-compose.yml

.env.example
pyproject.toml
README.md
```

## Implementation Order
1. Project structure + pyproject.toml
2. Core config (Pydantic Settings)
3. Core security (JWT utilities)
4. Models/schemas
5. Auth router
6. Health router
7. Middleware
8. App factory (main.py)
9. Dependencies
10. Docker setup
11. Tests
12. Documentation

---
*Generated: 2026-02-05*
*Status: Ready for implementation*
