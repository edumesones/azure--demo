# Architecture Overview - DataCatalog AI

## System Context

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                           │
│  Swagger UI / React Frontend / curl                         │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS + JWT
┌──────────────────────▼──────────────────────────────────────┐
│                   FastAPI (async)                            │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │ Auth     │  │ Ingestion    │  │ Query Engine           │  │
│  │ (OAuth/  │  │ Pipeline     │  │ (LangChain RAG)        │  │
│  │  JWT)    │  │ Service      │  │                        │  │
│  └──────────┘  └──────┬───────┘  └───────────┬───────────┘  │
└─────────────────────────┼────────────────────┼──────────────┘
                          │                    │
              ┌───────────▼──────┐   ┌─────────▼──────────┐
              │  Data Profiler   │   │  Vector DB          │
              │  (Pandas/NumPy)  │   │  (ChromaDB/Qdrant)  │
              └───────────┬──────┘   └─────────┬──────────┘
                          │                    │
              ┌───────────▼──────┐   ┌─────────▼──────────┐
              │  Azure Blob      │   │  Embedding Model    │
              │  Storage         │   │  (OpenAI / Azure    │
              │  (raw datasets)  │   │   OpenAI)           │
              └──────────────────┘   └────────────────────┘
```

## Tech Stack

| Layer | Technology | ADR |
|-------|------------|-----|
| API Framework | FastAPI (async) + Python 3.11 | [ADR-001](../decisions/ADR-001-fastapi.md) |
| Data Profiling | Pandas + NumPy | [ADR-002](../decisions/ADR-002-profiling.md) |
| RAG Framework | LangChain | [ADR-003](../decisions/ADR-003-langchain.md) |
| Vector Database | ChromaDB (dev) / Qdrant (prod) | [ADR-004](../decisions/ADR-004-vectordb.md) |
| Embeddings | OpenAI text-embedding-3-small | [ADR-005](../decisions/ADR-005-embeddings.md) |
| Authentication | JWT + OAuth2 (python-jose) | [ADR-006](../decisions/ADR-006-auth.md) |
| Storage | Azure Blob Storage | [ADR-007](../decisions/ADR-007-storage.md) |

## Project Structure

```
datacatalog-ai/
├── .github/workflows/          # CI/CD pipelines
├── docker/                     # Dockerfile + docker-compose
├── src/
│   ├── api/                    # FastAPI app + routers
│   │   ├── main.py             # App factory
│   │   ├── dependencies.py     # DI container
│   │   ├── middleware.py       # CORS, rate limiting
│   │   └── routers/            # Endpoint modules
│   ├── core/                   # Config, security, exceptions
│   ├── models/                 # Pydantic schemas + DB entities
│   ├── services/               # Business logic
│   │   ├── profiler.py         # Pandas profiling engine
│   │   ├── indexer.py          # Vector store operations
│   │   ├── rag_engine.py       # LangChain RAG pipeline
│   │   └── storage.py          # Azure Blob client
│   ├── chains/                 # LangChain chain definitions
│   └── utils/                  # Logging, metrics, PII detection
├── tests/                      # pytest suite
├── scripts/                    # Seed data, benchmarks
└── docs/                       # Documentation
```

## Key Patterns

- **Repository pattern** for data access
- **Service layer** for business logic
- **Dependency injection** via FastAPI Depends
- **Pydantic v2** for all validation
- **Async throughout** for non-blocking I/O

## Data Flow

### Dataset Onboarding
```
Upload CSV → Validate → Store in Blob → Profile (async) → Generate metadata → Embed → Index in Vector DB
```

### Natural Language Query
```
User query → Intent classification → Hybrid search (vector + filters) → Retrieve top-k → LLM generates answer → Return with citations
```

## Non-Functional Requirements

| Aspect | Target |
|--------|--------|
| NL query response (p95) | < 3 seconds |
| Dataset profiling (1M rows) | < 60 seconds |
| Semantic search (p95) | < 500ms |
| API throughput | 100 concurrent users |
| Test coverage | > 80% |

## Security

- JWT tokens with 24h expiry + refresh tokens
- HTTPS only
- RBAC: viewer / editor / admin roles
- PII detection and masking for non-admin users
- Input validation on all endpoints

---
*Last updated: 2026-02-05*
*ADRs: [View all](../decisions/)*
