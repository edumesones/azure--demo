# FEAT-001: Project Foundation - Critical Analysis

> **Analysis Depth:** Medium (Steps 1-2-3-5-9-11)
> **Rationale:** Well-known patterns (FastAPI, JWT, Docker) but new system foundation

---

## Step 1: Problem Clarification & Constraints

### Problem Statement
Create the foundational infrastructure for DataCatalog AI that enables rapid feature development with proper security, configuration, and observability from day one.

### Hard Constraints
- **Python 3.11+** - JD requirement
- **FastAPI** - Already decided in ADR-001
- **JWT authentication** - Stateless requirement for scaling
- **Docker** - Reproducible deployment requirement
- **Timeline** - 1 day for foundation (5-7 days total for MVP)

### Soft Constraints
- Prefer simplicity over flexibility for MVP
- In-memory user storage acceptable (no DB in this feature)
- Development-first (production hardening later)

### Success Criteria
- `docker-compose up` starts the API successfully
- Health endpoint responds < 50ms
- Token generation works with test credentials
- All endpoints documented in Swagger UI
- Basic pytest suite passes

### Non-Goals
- Production-grade user management (in-memory is fine)
- Rate limiting enforcement (middleware stub is enough)
- Complete CI/CD pipeline (that's FEAT-005)

---

## Step 2: Implicit Assumptions Identification

| # | Assumption | If Wrong, Impact | Confidence | Category |
|---|------------|------------------|------------|----------|
| 1 | Python 3.11 is available in deployment | Docker handles this | High | Environment |
| 2 | In-memory user store is sufficient for MVP | Would need DB earlier | High | Data |
| 3 | JWT secret can be loaded from env var | Security risk if hardcoded | High | Security |
| 4 | No need for async DB driver yet | Correct, no DB in this feature | High | Technical |
| 5 | CORS origins can be configured via env | Standard practice | High | Security |
| 6 | Hot-reload works with uvicorn --reload | Standard FastAPI setup | High | Development |
| 7 | Pydantic v2 syntax is stable | May need adjustment | Medium | Technical |
| 8 | Rate limiting can be deferred | OK for demo, risky for prod | Medium | Security |

### Assumptions Requiring Validation
- None critical - all assumptions have Medium-High confidence

---

## Step 3: Design Space Exploration

### Approach A: Minimal FastAPI Setup
**Core idea:** Bare minimum FastAPI app with inline configuration
**Pros:** Fastest to implement, simple
**Cons:** Hard to maintain, no separation of concerns
**Best when:** Throwaway prototypes
**Effort:** Low

### Approach B: Application Factory Pattern (RECOMMENDED)
**Core idea:** FastAPI app created via factory function with proper module separation
```
src/
├── api/main.py          # create_app() factory
├── api/routers/         # Endpoint modules
├── core/config.py       # Pydantic Settings
├── core/security.py     # JWT logic
```
**Pros:**
- Testable (can create app with different configs)
- Scalable structure
- Clear separation of concerns
- Industry standard pattern
**Cons:** More initial setup
**Best when:** Production-intent projects
**Effort:** Medium

### Approach C: Full Microservices Setup
**Core idea:** Separate services for auth, API gateway, etc.
**Pros:** Maximum scalability
**Cons:** Massive overkill for MVP, complexity explosion
**Best when:** Large teams, high scale
**Effort:** High

### Preliminary Recommendation
**Approach B: Application Factory Pattern** - Right balance of structure and simplicity for a portfolio project that needs to demonstrate professional practices.

---

## Step 5: Failure-First Analysis

### Critical Failures (High Severity)

| Failure Mode | Probability | Severity | Detection | Mitigation |
|--------------|-------------|----------|-----------|------------|
| JWT secret exposed in code | Low | Critical | Code review, secrets scan | Load from env var only |
| App fails to start | Medium | High | Health check fails | Proper error handling in startup |
| Auth bypass vulnerability | Low | Critical | Security testing | Use proven libraries (python-jose) |

### Likely Failures (High Probability)

| Failure Mode | Probability | Severity | Detection | Mitigation |
|--------------|-------------|----------|-----------|------------|
| Missing env vars crash app | High | Medium | Startup failure | Pydantic Settings validation with clear errors |
| CORS blocks frontend | High | Low | Browser console | Configurable CORS origins |
| Token expiry too short/long | Medium | Low | User complaints | Configurable expiry via env |
| Docker build fails | Medium | Medium | CI pipeline | Multi-stage build, pin versions |

### Cascading Failures
- If config loading fails → App won't start → No health check → Container restarts loop
- If JWT secret is weak → Tokens can be forged → Complete auth bypass

---

## Step 9: Adversarial Review (Paranoid Staff Engineer Mode)

### Over-engineering Concerns
- **Rate limiting middleware**: For MVP demo, a simple stub is fine. Don't implement Redis-backed rate limiting yet.
- **User management**: In-memory dict with 3 test users is perfect. No need for SQLAlchemy/database yet.
- **OAuth2 flows**: OAuth2PasswordBearer is enough. Skip actual OAuth2 provider integration.

### Under-engineering Concerns
- **JWT secret handling**: MUST be from env var, never hardcoded. Add validation that it's at least 32 chars.
- **Password hashing**: MUST use bcrypt via passlib, not plain text even for demo.
- **Error responses**: Should be structured JSON, not default FastAPI errors.

### The 2AM Incident
**Most likely:** "JWT_SECRET not set in production deployment, app starts with default secret, tokens can be forged."
**Prevention:** Fail fast if JWT_SECRET is not set or is the default value.

### Future Pain Points
- In-memory user store will need migration to DB (but that's expected)
- No refresh token rotation (acceptable for MVP)

### Security Concerns
- **Token in URL**: Ensure tokens only in Authorization header
- **Timing attacks**: Use constant-time comparison for passwords
- **Error messages**: Don't reveal whether email exists on login failure

### Scale Concerns
- In-memory storage is fine for MVP (stateless JWT means no session scaling issues)
- Health endpoint should not do expensive checks

### Red Flags Found
- None critical. Design is sound for MVP scope.

---

## Step 11: Decision Summary

### Recommended Approach
**Application Factory Pattern** with:
- `src/api/main.py` - FastAPI app factory
- `src/core/config.py` - Pydantic Settings
- `src/core/security.py` - JWT utilities
- `src/api/routers/auth.py` - Auth endpoints
- `src/api/routers/health.py` - Health/metrics endpoints

### Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| App structure | Factory pattern | Testable, scalable, professional |
| User storage | In-memory dict | MVP scope, no DB needed yet |
| JWT library | python-jose | Proven, well-maintained |
| Password hashing | passlib[bcrypt] | Industry standard |
| Config | Pydantic Settings v2 | Type-safe, validation built-in |
| Logging | structlog | JSON output, correlation IDs |

### Short-term Goals (This Implementation)
1. Working FastAPI app with health endpoint
2. JWT auth with 3 test users (admin, editor, viewer)
3. Docker Compose for one-command startup
4. Basic pytest setup with auth tests

### Long-term Considerations
- User storage will migrate to PostgreSQL in FEAT-002
- Rate limiting will need Redis for production
- OAuth2 provider integration for enterprise

### Remaining Unknowns
- [x] All unknowns resolved

### Security Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| JWT secret leak | Low | Critical | Env var only, validation |
| Brute force login | Medium | Medium | Rate limiting (future) |
| Token theft | Low | High | HTTPS, short expiry |

### Blast Radius Analysis
- If auth service fails: All protected endpoints unavailable
- If config fails: App won't start (contained failure)
- Maximum blast radius: API unavailable (acceptable for single-service MVP)

### Confidence Level
**High** - Well-understood patterns, proven libraries, clear scope boundaries.

### Red Flags to Watch
- JWT_SECRET must never be committed to repo
- Don't add database complexity in this feature
- Keep middleware simple (stubs OK)

### Recommended Next Steps
1. Proceed to **Plan** phase
2. Generate `design.md` with file structure
3. Generate `tasks.md` with ~15-20 tasks
4. Create branch `feature/001-foundation`
5. Implement

---

*Analysis completed: 2026-02-05*
*Analyst: Claude*
*Confidence: High*
*Red flags: 0 critical*
