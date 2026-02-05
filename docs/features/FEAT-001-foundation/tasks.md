# FEAT-001: Project Foundation - Tasks

## Progress

| Section | Progress | Tasks |
|---------|----------|-------|
| Setup | ⬜ 0% | 0/4 |
| Core | ⬜ 0% | 0/4 |
| API | ⬜ 0% | 0/5 |
| Docker | ⬜ 0% | 0/2 |
| Tests | ⬜ 0% | 0/2 |
| Docs | ⬜ 0% | 0/1 |
| **Total** | ⬜ 0% | 0/18 |

## Status Legend
- `[ ]` Pending
- `[🟡]` In Progress
- `[x]` Complete
- `[🔴]` Blocked (reason)
- `[⏭️]` Skipped (reason)

---

## Setup Tasks

- [ ] S1: Create project structure (src/, tests/, docker/)
- [ ] S2: Create pyproject.toml with dependencies
- [ ] S3: Create .env.example with all required variables
- [ ] S4: Create src/__init__.py and subpackage inits

---

## Core Tasks

- [ ] C1: Create src/core/config.py (Pydantic Settings)
- [ ] C2: Create src/core/security.py (JWT utilities + password hashing)
- [ ] C3: Create src/core/exceptions.py (custom exceptions)
- [ ] C4: Create src/models/schemas.py (User, Token, TokenPayload)

---

## API Tasks

- [ ] A1: Create src/api/routers/auth.py (POST /token, /refresh, GET /me)
- [ ] A2: Create src/api/routers/health.py (GET /health, /ready, /metrics)
- [ ] A3: Create src/api/middleware.py (CORS, logging, correlation ID)
- [ ] A4: Create src/api/dependencies.py (get_current_user, require_role)
- [ ] A5: Create src/api/main.py (create_app factory)

---

## Docker Tasks

- [ ] D1: Create docker/Dockerfile (multi-stage build)
- [ ] D2: Create docker/docker-compose.yml (dev environment)

---

## Tests

- [ ] T1: Create tests/conftest.py (fixtures, test client)
- [ ] T2: Create tests/test_auth.py (auth endpoint tests)

---

## Documentation

- [ ] DOC1: Update README.md with setup instructions

---

## Blockers & Decisions

| Issue | Status | Resolution |
|-------|--------|------------|
| (none) | - | - |

---
*Generated: 2026-02-05*
*Total tasks: 18*
*Estimated effort: 1 day*
