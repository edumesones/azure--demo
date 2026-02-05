# Project: DataCatalog AI

## Vision

**One-liner:** Intelligent, self-service data catalog that enables natural language querying of enterprise datasets via RAG.

**Problem:** Enterprise data teams spend 30-40% of their time finding and understanding data. Metadata is scattered across tools, tribal knowledge exists only in people's heads, and there's no visibility into data quality.

**Solution:** A unified, queryable knowledge layer over all data assets, accessible through natural language. "Google for your data lake."

**Success criteria:**
- Query accuracy >85% on demo queries
- Time to demo < 5 min from `docker-compose up`
- Test coverage >80%
- 90%+ JD keyword coverage demonstrated

## Users

| Persona | Need | Example Query |
|---------|------|---------------|
| **Data Analyst** | Find the right table for a report | "Which tables contain monthly revenue by region?" |
| **Data Engineer** | Understand lineage and dependencies | "What upstream sources feed the customer_360 table?" |
| **Business User** | Understand data meaning and quality | "How fresh is the sales data? Are there any known issues?" |
| **Data Governance Lead** | Audit quality and compliance | "Show me all PII columns across the warehouse" |

**Technical level:** Intermediate to Expert

## Core Features (MVP)

1. **Data Ingestion & Profiling** - Upload CSV, auto-profile schema, stats, quality metrics, PII detection
2. **Metadata Indexing** - Embed metadata in vector store (ChromaDB), hybrid search
3. **Natural Language Query (RAG)** - LangChain RAG pipeline with intent classification, citations
4. **API Layer** - FastAPI async endpoints for all operations
5. **Authentication & RBAC** - JWT + OAuth2, viewer/editor/admin roles

## Technical Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Language | Python 3.11+ | JD requirement, team expertise |
| Framework | FastAPI (async) | High performance, auto-docs, native async |
| Data Profiling | Pandas + NumPy | Industry standard, rich capabilities |
| RAG Framework | LangChain | Mature ecosystem, modular chains |
| Vector DB | ChromaDB (dev) / Qdrant (prod) | ChromaDB simple, Qdrant scales |
| Embeddings | OpenAI text-embedding-3-small | Cost-effective, high quality |
| LLM | GPT-4o / Azure OpenAI | Best reasoning for metadata queries |
| Auth | python-jose + passlib | JWT + OAuth2 standard |
| Storage | Azure Blob Storage | Dataset file storage |
| Containerization | Docker + Docker Compose | Reproducible deployment |
| Testing | pytest + pytest-asyncio | Async-native testing |
| CI/CD | GitHub Actions | Automated pipeline |

## Constraints

- **Timeline:** 5-7 days (portfolio project)
- **Budget:** Minimize LLM API costs (use gpt-4o-mini for dev)
- **Team:** Solo developer
- **Compliance:** PII detection and masking required

## Out of Scope (v1)

- Production Qdrant deployment
- Full Azure Functions integration (stubbed)
- React frontend (API-only for demo)
- Real OAuth2 provider integration (simulated)
- Multi-tenant isolation
- Real-time streaming profiling
- Scheduled re-profiling cron jobs

## Risks & Unknowns

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM API costs during development | Medium | Use gpt-4o-mini for dev, mock in tests |
| ChromaDB performance at scale | Low (demo) | Document Qdrant migration path |
| Azure service setup complexity | Medium | Docker-compose for local, stubs for demo |
| Demo data realism | Medium | Use Faker with domain-specific generators |

## Open Questions

- [x] All questions resolved in PRD

## Demo Datasets

| Dataset | Rows | Columns | Domain |
|---------|------|---------|--------|
| ecommerce_orders | 100K | 15 | Sales |
| customer_profiles | 50K | 22 | CRM |
| product_catalog | 5K | 18 | Inventory |
| marketing_campaigns | 10K | 12 | Marketing |
| web_analytics_events | 500K | 8 | Digital |

---
*Interview completed: 2026-02-05*
*Source: PRD_DataCatalog.md*
*Ready for: Architecture definition*
