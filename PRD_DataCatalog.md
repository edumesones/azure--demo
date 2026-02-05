# Product Requirements Document (PRD)

## DataCatalog AI — Intelligent Data Catalog with Natural Language Querying

| Field | Value |
|---|---|
| **Author** | Glemes |
| **Version** | 1.0 |
| **Date** | 2025-02-05 |
| **Status** | Draft |

---

## 1. Executive Summary

DataCatalog AI is an intelligent, self-service data catalog that automatically profiles enterprise datasets, indexes their metadata (schemas, lineage, quality metrics) into a vector database, and enables natural language querying via a RAG-powered conversational interface. The system empowers data analysts, engineers, and business users to discover, understand, and assess data assets without writing SQL or navigating complex metadata repositories.

Built with FastAPI, LangChain, and Azure cloud services, the platform combines automated data profiling with semantic search to create a "Google for your data lake" experience.

---

## 2. Problem Statement

Enterprise data teams face recurring challenges:

- **Data discovery is slow**: analysts spend 30-40% of their time finding and understanding data before doing actual analysis.
- **Metadata is scattered**: schema definitions, lineage, quality reports, and ownership information live in disconnected tools and wikis.
- **Tribal knowledge**: critical context about datasets (known issues, recommended joins, business definitions) exists only in people's heads.
- **Quality blind spots**: teams consume datasets without visibility into freshness, completeness, or anomaly history.

DataCatalog AI solves this by creating a unified, queryable knowledge layer over all data assets, accessible through natural language.

---

## 3. Target Users

| Persona | Need | Example Query |
|---|---|---|
| **Data Analyst** | Find the right table for a report | *"Which tables contain monthly revenue by region?"* |
| **Data Engineer** | Understand lineage and dependencies | *"What upstream sources feed the customer_360 table?"* |
| **Business User** | Understand data meaning and quality | *"How fresh is the sales data? Are there any known issues?"* |
| **Data Governance Lead** | Audit quality and compliance | *"Show me all PII columns across the warehouse"* |

---

## 4. Architecture Overview

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

---

## 5. Functional Requirements

### 5.1 Data Ingestion & Profiling Pipeline

**FR-1**: The system SHALL accept dataset uploads via API (CSV, Parquet, JSON) and store raw files in Azure Blob Storage.

**FR-2**: The system SHALL automatically profile each dataset upon ingestion, generating:
- Schema metadata: column names, data types, nullable flags
- Statistical profile: row count, cardinality, min/max, mean/std, percentiles (numeric), top-k values (categorical)
- Quality metrics: null percentage, duplicate rate, uniqueness ratio, pattern detection (emails, dates, IDs)
- Inferred semantic tags: PII detection (email, phone, SSN patterns), temporal columns, categorical vs continuous

**FR-3**: The system SHALL allow manual enrichment of metadata:
- Business descriptions for tables and columns
- Lineage declarations (upstream/downstream dependencies)
- Tags and domain classification (finance, marketing, HR, etc.)
- Known issues and caveats
- Owner assignment

**FR-4**: The system SHALL support incremental re-profiling when datasets are updated, computing delta metrics (drift detection).

### 5.2 Metadata Indexing & Vector Store

**FR-5**: The system SHALL generate structured metadata documents per dataset/table combining schema, profile, quality, lineage, and business context into a unified representation.

**FR-6**: The system SHALL chunk and embed metadata documents using a configurable embedding model (default: `text-embedding-3-small`) and store them in a vector database (ChromaDB for dev, Qdrant for production).

**FR-7**: The system SHALL maintain a metadata versioning system, preserving historical profiles for drift analysis.

**FR-8**: The system SHALL support hybrid search: dense vector similarity + keyword filtering on structured fields (domain, owner, tags, quality score).

### 5.3 Natural Language Query Engine (RAG)

**FR-9**: The system SHALL accept natural language queries about data assets and return contextual, sourced answers using LangChain's RAG pipeline.

**FR-10**: The RAG pipeline SHALL implement:
- Query understanding: intent classification (discovery, quality, lineage, definition)
- Retrieval: hybrid search with configurable top-k and similarity threshold
- Context augmentation: retrieved metadata formatted with structured prompts
- Generation: LLM response with source citations (which datasets/columns informed the answer)
- Conversation memory: multi-turn context within a session

**FR-11**: The system SHALL support the following query patterns:
- **Discovery**: *"Find tables with customer purchase history"*
- **Quality assessment**: *"What's the data quality score for the orders table?"*
- **Lineage**: *"What feeds into the revenue_dashboard dataset?"*
- **Schema exploration**: *"What columns does the users table have? Which are nullable?"*
- **Cross-dataset**: *"Which tables can I join to get customer demographics with transaction data?"*
- **Comparative**: *"Compare data freshness across all marketing datasets"*

**FR-12**: The system SHALL return structured responses including:
- Natural language answer
- Source datasets/tables referenced
- Confidence score
- Suggested follow-up queries

### 5.4 API Layer

**FR-13**: The system SHALL expose a RESTful API via FastAPI with the following endpoint groups:

| Group | Endpoints | Description |
|---|---|---|
| **Auth** | `POST /auth/token`, `POST /auth/refresh` | JWT-based authentication with OAuth2 support |
| **Datasets** | `POST /datasets/`, `GET /datasets/{id}`, `PATCH /datasets/{id}`, `DELETE /datasets/{id}` | CRUD for dataset registration and metadata |
| **Ingestion** | `POST /datasets/{id}/upload`, `POST /datasets/{id}/profile` | Upload files and trigger profiling |
| **Search** | `POST /search/query`, `POST /search/semantic`, `GET /search/filters` | NL query, vector search, and filter options |
| **Lineage** | `GET /lineage/{dataset_id}`, `POST /lineage/` | View and declare data lineage |
| **Quality** | `GET /quality/{dataset_id}`, `GET /quality/dashboard` | Quality metrics and aggregated dashboard |
| **Admin** | `GET /health`, `GET /metrics` | Health checks and performance metrics |

**FR-14**: All endpoints SHALL be async (`async def`) for non-blocking I/O operations.

**FR-15**: The API SHALL implement rate limiting, request validation (Pydantic v2), and structured error responses.

### 5.5 Security

**FR-16**: The system SHALL implement JWT-based authentication with configurable token expiry and refresh tokens.

**FR-17**: The system SHALL support OAuth2 integration for enterprise SSO.

**FR-18**: The system SHALL enforce role-based access control (RBAC):
- `viewer`: read-only access to metadata and search
- `editor`: can enrich metadata, declare lineage
- `admin`: full access including dataset deletion and user management

**FR-19**: The system SHALL mask or redact PII columns in API responses for non-admin users.

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target |
|---|---|
| NL query response (p95) | < 3 seconds |
| Dataset profiling (1M rows) | < 60 seconds |
| Semantic search (p95) | < 500ms |
| API throughput | 100 concurrent users |
| Embedding indexing | < 5s per dataset metadata doc |

### 6.2 Scalability

- Horizontal scaling via Azure Container Instances or AKS
- Vector DB supports 100K+ metadata documents
- Async profiling jobs via background task queue

### 6.3 Reliability

- 99.5% API uptime target
- Graceful degradation: if LLM is unavailable, fall back to keyword search
- Retry logic for Azure services and LLM API calls

### 6.4 Observability

- Structured logging (JSON) with correlation IDs
- Prometheus-compatible metrics endpoint
- LLM call tracing (LangSmith integration)
- Profiling performance tracking per dataset

---

## 7. Technical Stack

| Component | Technology | Rationale |
|---|---|---|
| **API Framework** | FastAPI (async) | High performance, auto-docs, native async |
| **Data Profiling** | Pandas + NumPy | Industry standard, rich profiling capabilities |
| **RAG Framework** | LangChain | Mature ecosystem, modular chain composition |
| **Vector Database** | ChromaDB (dev) / Qdrant (prod) | ChromaDB for simplicity, Qdrant for scale |
| **Embeddings** | OpenAI `text-embedding-3-small` / Azure OpenAI | Cost-effective, high quality |
| **LLM** | GPT-4o / Azure OpenAI | Best reasoning for complex metadata queries |
| **Authentication** | `python-jose` + `passlib` | JWT + OAuth2 standard implementation |
| **Cloud Storage** | Azure Blob Storage | Dataset file storage |
| **Serverless** | Azure Functions | Async profiling triggers |
| **Containerization** | Docker + Docker Compose | Reproducible deployment |
| **Testing** | pytest + pytest-asyncio | Async-native testing |
| **CI/CD** | GitHub Actions | Automated test, lint, build, deploy |
| **Monitoring** | Prometheus + LangSmith | Metrics + LLM observability |

---

## 8. Data Model

### 8.1 Core Entities

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│   Dataset    │1────*│    Column         │       │   Lineage    │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id           │       │ id               │       │ id           │
│ name         │       │ dataset_id (FK)  │       │ source_id    │
│ description  │       │ name             │       │ target_id    │
│ domain       │       │ dtype            │       │ relationship │
│ owner        │       │ nullable         │       │ description  │
│ tags[]       │       │ description      │       └──────────────┘
│ source_type  │       │ semantic_tags[]  │
│ file_path    │       │ is_pii          │       ┌──────────────┐
│ created_at   │       │ stats (JSON)    │       │ QualityReport│
│ updated_at   │       └──────────────────┘       ├──────────────┤
│ quality_score│                                   │ id           │
└──────────────┘                                   │ dataset_id   │
                                                   │ row_count    │
                                                   │ null_rate    │
                                                   │ duplicate_rate│
                                                   │ freshness    │
                                                   │ anomalies[]  │
                                                   │ profiled_at  │
                                                   └──────────────┘
```

### 8.2 Vector Store Schema

Each metadata document indexed in the vector store follows this structure:

```json
{
  "id": "dataset_{uuid}_v{version}",
  "text": "Unified natural language representation of the dataset metadata",
  "metadata": {
    "dataset_id": "uuid",
    "dataset_name": "string",
    "domain": "string",
    "owner": "string",
    "tags": ["string"],
    "quality_score": 0.85,
    "row_count": 1000000,
    "column_count": 25,
    "has_pii": true,
    "last_profiled": "2025-01-15T10:30:00Z",
    "version": 3
  }
}
```

---

## 9. Key User Flows

### 9.1 Dataset Onboarding

```
User uploads CSV ──▶ API validates & stores in Azure Blob
                          │
                          ▼
                    Profiling job triggered (async)
                          │
                          ▼
                    Pandas reads file ──▶ Compute schema + stats + quality
                          │
                          ▼
                    Generate metadata document
                          │
                          ▼
                    Embed & index in vector store
                          │
                          ▼
                    Dataset available for NL queries
```

### 9.2 Natural Language Query

```
User asks: "Which datasets have customer email addresses?"
                          │
                          ▼
              Query Understanding (intent: discovery, entity: email, PII)
                          │
                          ▼
              Hybrid Search: vector similarity + filter(has_pii=true)
                          │
                          ▼
              Top-k metadata docs retrieved (k=5)
                          │
                          ▼
              LLM generates answer with citations
                          │
                          ▼
              Response: "3 datasets contain email columns:
               - customers (col: email, contact_email)
               - leads (col: lead_email)
               - newsletter_subscribers (col: subscriber_email)
               All are tagged as PII. The customers table has
               the highest quality score (0.92)."
```

---

## 10. Project Structure

```
datacatalog-ai/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint + test on PR
│       └── cd.yml                    # Build + deploy on merge
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app factory
│   │   ├── dependencies.py           # Dependency injection
│   │   ├── middleware.py             # CORS, rate limiting, logging
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── datasets.py
│   │       ├── ingestion.py
│   │       ├── search.py
│   │       ├── lineage.py
│   │       └── quality.py
│   ├── core/
│   │   ├── config.py                 # Pydantic Settings
│   │   ├── security.py               # JWT + OAuth2
│   │   └── exceptions.py
│   ├── models/
│   │   ├── schemas.py                # Pydantic request/response models
│   │   └── database.py               # SQLAlchemy / SQLModel entities
│   ├── services/
│   │   ├── profiler.py               # Pandas/NumPy profiling engine
│   │   ├── indexer.py                # Embedding + vector store indexing
│   │   ├── rag_engine.py            # LangChain RAG pipeline
│   │   ├── query_router.py          # Intent classification + routing
│   │   └── storage.py               # Azure Blob Storage client
│   ├── chains/
│   │   ├── discovery_chain.py        # Dataset discovery queries
│   │   ├── quality_chain.py          # Quality assessment queries
│   │   ├── lineage_chain.py          # Lineage exploration queries
│   │   └── prompts/
│   │       ├── system.py
│   │       ├── discovery.py
│   │       └── quality.py
│   └── utils/
│       ├── logging.py
│       ├── metrics.py
│       └── pii_detector.py
├── tests/
│   ├── conftest.py                   # Fixtures, async client
│   ├── unit/
│   │   ├── test_profiler.py
│   │   ├── test_rag_engine.py
│   │   └── test_security.py
│   ├── integration/
│   │   ├── test_ingestion_flow.py
│   │   └── test_search_flow.py
│   └── fixtures/
│       └── sample_datasets/
├── azure/
│   ├── function_app.py               # Azure Function for async profiling
│   └── host.json
├── scripts/
│   ├── seed_demo_data.py
│   └── benchmark_search.py
├── docs/
│   ├── api_reference.md
│   ├── architecture.md
│   └── deployment.md
├── .env.example
├── pyproject.toml
├── Makefile
└── README.md
```

---

## 11. Demo Scope (MVP)

For portfolio/interview purposes, the MVP delivers a focused vertical slice:

### In Scope (MVP)

- [x] Dataset upload (CSV) + automatic profiling with Pandas
- [x] Metadata embedding and indexing in ChromaDB
- [x] Natural language query endpoint with LangChain RAG
- [x] Hybrid search (vector + metadata filters)
- [x] JWT authentication with RBAC (viewer/editor/admin)
- [x] 3-5 pre-loaded demo datasets with rich metadata
- [x] Async endpoints throughout
- [x] Docker Compose for local deployment
- [x] pytest suite (unit + integration, >80% coverage)
- [x] CI pipeline with GitHub Actions
- [x] Swagger/OpenAPI documentation
- [x] Structured logging + basic metrics endpoint

### Out of Scope (Future)

- [ ] Production Qdrant deployment
- [ ] Full Azure Functions integration (stubbed)
- [ ] React frontend (API-only for demo)
- [ ] Real OAuth2 provider integration (simulated)
- [ ] Multi-tenant isolation
- [ ] Real-time streaming profiling
- [ ] Scheduled re-profiling cron jobs

---

## 12. Demo Datasets

The project ships with synthetic but realistic demo data:

| Dataset | Rows | Columns | Domain | Highlights |
|---|---|---|---|---|
| `ecommerce_orders` | 100K | 15 | Sales | Revenue, dates, customer IDs |
| `customer_profiles` | 50K | 22 | CRM | PII columns, demographics |
| `product_catalog` | 5K | 18 | Inventory | Categories, pricing, descriptions |
| `marketing_campaigns` | 10K | 12 | Marketing | Campaign metrics, A/B test flags |
| `web_analytics_events` | 500K | 8 | Digital | Clickstream, sessions, timestamps |

Each dataset includes pre-computed lineage relationships (e.g., `ecommerce_orders` depends on `customer_profiles` and `product_catalog`).

---

## 13. JD Coverage Matrix

| JD Requirement | How Covered |
|---|---|
| Python backend | Entire backend in Python 3.11+ |
| FastAPI | Core API framework, async throughout |
| Pandas / NumPy | Data profiling engine |
| RAG | LangChain RAG pipeline for NL queries |
| Prompt Engineering | Specialized prompts per query intent |
| Vector databases | ChromaDB (dev) / Qdrant (prod) |
| Embedding models | OpenAI text-embedding-3-small, configurable |
| LangChain | Core RAG framework |
| Large datasets | Profiling engine handles 100K-500K row datasets |
| Data cleaning/transformation | Profiler includes type inference, null handling |
| Azure Cloud Services | Blob Storage, Azure Functions (stub) |
| Async programming | Full async FastAPI + async LangChain calls |
| Docker | Dockerfile + docker-compose.yml |
| OAuth / JWT | JWT auth with OAuth2-compatible flow |
| AI ethics / responsible AI | PII detection, RBAC-based data masking |
| Data engineering concepts | Lineage tracking, data quality pipelines |
| Performance monitoring | Prometheus metrics, LangSmith tracing |
| pytest | Unit + integration test suite |
| CI/CD | GitHub Actions pipelines |

---

## 14. Success Metrics

| Metric | Target |
|---|---|
| JD keyword coverage | 90%+ of required skills demonstrated |
| Test coverage | >80% |
| Query accuracy (manual eval) | >85% relevant answers on demo queries |
| Time to demo | < 5 min from `docker-compose up` to first query |
| Code quality | Ruff clean, mypy strict, no security warnings |

---

## 15. Milestones

| Phase | Deliverables | Estimated Effort |
|---|---|---|
| **Phase 1 — Foundation** | Project scaffolding, config, Docker, auth, health endpoint | 1 day |
| **Phase 2 — Profiling** | Upload endpoint, Pandas profiler, metadata models | 1-2 days |
| **Phase 3 — Indexing** | Embedding pipeline, ChromaDB integration, hybrid search | 1 day |
| **Phase 4 — RAG Engine** | LangChain chains, prompt templates, query router | 1-2 days |
| **Phase 5 — Polish** | Demo data, tests, CI/CD, documentation, README | 1 day |

**Total estimated effort: 5-7 days**

---

## 16. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| LLM API costs during development | Medium | Use `gpt-4o-mini` for dev, mock responses in tests |
| ChromaDB performance at scale | Low (demo) | Document Qdrant migration path |
| Azure service setup complexity | Medium | Docker-compose for local dev, Azure stubs for demo |
| Embedding model changes | Low | Abstract behind interface, configurable via env vars |
| Demo data realism | Medium | Use Faker with domain-specific generators |
