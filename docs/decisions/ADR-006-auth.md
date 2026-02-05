# ADR-006: Use JWT + OAuth2 for Authentication

## Status
Accepted

## Date
2026-02-05

## Context
We need authentication and authorization for the API. Requirements:
- Secure token-based authentication
- Role-based access control (RBAC)
- OAuth2 compatibility for enterprise SSO
- Stateless for horizontal scaling

## Options Considered

### Option 1: JWT with python-jose + passlib
**Pros:**
- Industry standard
- Stateless authentication
- OAuth2 compatible flow
- Well-documented libraries
- FastAPI has built-in OAuth2 support

**Cons:**
- Token revocation requires additional infrastructure

### Option 2: Session-based auth
**Pros:**
- Simple to implement
- Easy revocation

**Cons:**
- Requires session storage
- Not stateless
- Poor for microservices

### Option 3: API Keys only
**Pros:**
- Very simple

**Cons:**
- No user identity
- No RBAC support
- Not OAuth2 compatible

## Decision
**JWT with python-jose + passlib** - Industry standard, stateless, OAuth2 compatible.

## Consequences
- Implement JWT tokens with 24h expiry
- Refresh tokens with 7d expiry
- RBAC with three roles: viewer, editor, admin
- PII masking based on role
- OAuth2 password flow for demo (enterprise SSO stubbed)

## RBAC Matrix

| Action | viewer | editor | admin |
|--------|--------|--------|-------|
| Search metadata | ✅ | ✅ | ✅ |
| View datasets | ✅ | ✅ | ✅ |
| Upload datasets | ❌ | ✅ | ✅ |
| Edit metadata | ❌ | ✅ | ✅ |
| Delete datasets | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |
| View PII columns | ❌ | ❌ | ✅ |

## Implementation
```python
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return User(**payload)
```
