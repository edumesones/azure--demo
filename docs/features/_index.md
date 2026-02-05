# Features Dashboard - DataCatalog AI

## MVP Scope

**Target:** Portfolio demo (5-7 days)
**Status:** Planning

## Feature List

### MVP (Must Have)

| ID | Feature | Status | Phase | Progress | Priority | Est. Effort |
|----|---------|--------|-------|----------|----------|-------------|
| FEAT-001-foundation | Project Foundation | 🟡 In Progress | Think Critically ✅ | - | P0 | 1 day |
| FEAT-002-profiling | Data Profiling Pipeline | ⚪ Pending | - | - | P0 | 1-2 days |
| FEAT-003-indexing | Metadata Indexing & Vector Store | ⚪ Pending | - | - | P0 | 1 day |
| FEAT-004-rag | RAG Query Engine | ⚪ Pending | - | - | P0 | 1-2 days |
| FEAT-005-polish | Demo Data & Polish | ⚪ Pending | - | - | P0 | 1 day |

### Feature Descriptions

#### FEAT-001-foundation
Project scaffolding, config management, Docker setup, authentication (JWT/OAuth2), health endpoints, basic middleware (CORS, rate limiting, logging).

#### FEAT-002-profiling
Dataset upload endpoint (CSV/Parquet/JSON), Azure Blob Storage integration, Pandas/NumPy profiling engine, metadata models, quality metrics, PII detection.

#### FEAT-003-indexing
Embedding generation pipeline, ChromaDB integration, metadata document structure, hybrid search (vector + filters), versioning support.

#### FEAT-004-rag
LangChain RAG pipeline, intent classification (discovery/quality/lineage), prompt templates, query router, response formatting with citations, conversation memory.

#### FEAT-005-polish
Demo datasets (5 synthetic datasets), seed scripts, pytest suite (>80% coverage), CI/CD pipeline, documentation, README.

## Dependencies

```
FEAT-001-foundation ────┐
                        ├──► FEAT-002-profiling ────┐
                        │                           ├──► FEAT-004-rag
                        └──► FEAT-003-indexing ─────┘
                                                    │
                                                    ▼
                                            FEAT-005-polish
```

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⚪ | Pending - Not started |
| 🟡 | In Progress - Active work |
| 🔵 | In Review - PR open |
| 🟢 | Complete - Merged |
| 🔴 | Blocked - Needs attention |

## Timeline

```
Day 1:   FEAT-001-foundation [████████████████████] 100%
Day 2-3: FEAT-002-profiling  [░░░░░░░░░░░░░░░░░░░░] 0%
Day 3-4: FEAT-003-indexing   [░░░░░░░░░░░░░░░░░░░░] 0%
Day 4-5: FEAT-004-rag        [░░░░░░░░░░░░░░░░░░░░] 0%
Day 6-7: FEAT-005-polish     [░░░░░░░░░░░░░░░░░░░░] 0%
```

## Out of Scope (Post-MVP)

- Production Qdrant deployment
- Full Azure Functions integration
- React frontend
- Real OAuth2 provider integration
- Multi-tenant isolation
- Real-time streaming profiling

---
*Last updated: 2026-02-05*
*MVP target: 5-7 days*
