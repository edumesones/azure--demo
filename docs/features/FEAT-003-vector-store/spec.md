# FEAT-003: Vector Store Integration - Specification

## Overview
Integrate ChromaDB as the vector store for semantic search capabilities. Implement embedding generation using OpenAI's text-embedding-3-small model and create API endpoints for searching catalog metadata using natural language.

## User Stories

### US-1: Embedding Generation
**As a** system
**I want** to generate embeddings for catalog metadata
**So that** users can search using natural language

**Acceptance Criteria:**
- [ ] Generate embeddings for table descriptions
- [ ] Generate embeddings for column descriptions
- [ ] Batch processing for efficiency
- [ ] Store embeddings in ChromaDB

### US-2: Semantic Search
**As a** data analyst
**I want** to search the catalog using natural language
**So that** I can find relevant tables and columns quickly

**Acceptance Criteria:**
- [ ] POST /api/v1/search endpoint
- [ ] Return ranked results with similarity scores
- [ ] Filter by data source (optional)
- [ ] Pagination support

### US-3: Index Management
**As an** admin
**I want** to manage the vector index
**So that** I can rebuild or update embeddings

**Acceptance Criteria:**
- [ ] POST /api/v1/index/rebuild endpoint (admin only)
- [ ] Background indexing for large catalogs
- [ ] Index status endpoint

## Technical Decisions

| # | Area | Question | Decision | Notes |
|---|------|----------|----------|-------|
| 1 | Vector DB | Which vector store? | ChromaDB | Simple, embedded, good for MVP |
| 2 | Embeddings | Which model? | text-embedding-3-small | Cost-effective, good quality |
| 3 | Client | OpenAI client? | openai Python SDK | Official, async support |
| 4 | Storage | Persistence? | Local directory | ./chroma_data |
| 5 | Batch Size | Embedding batch? | 100 items | Balance speed/memory |

## Scope

### In Scope
- ChromaDB client setup and configuration
- OpenAI embedding service
- Embedding generation for tables and columns
- Semantic search endpoint
- Index rebuild endpoint
- Search result ranking

### Out of Scope
- Real-time embedding updates (batch only for MVP)
- Multiple embedding models
- Hybrid search (semantic + keyword)
- RAG/LLM integration (FEAT-004)

## Dependencies
- FEAT-001: Project Foundation (completed)
- FEAT-002: Database Layer (completed)
- OpenAI API key required

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/v1/search | Semantic search | Yes |
| GET | /api/v1/search/suggestions | Search suggestions | Yes |
| POST | /api/v1/index/rebuild | Rebuild vector index | Admin |
| GET | /api/v1/index/status | Get index status | Admin |

## Data Models

### SearchRequest
```python
class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    data_source_id: UUID | None = None
    include_columns: bool = True
```

### SearchResult
```python
class SearchResult(BaseModel):
    id: UUID
    type: Literal["table", "column"]
    name: str
    description: str | None
    similarity_score: float
    data_source_name: str
    table_name: str | None  # For columns
```

### IndexStatus
```python
class IndexStatus(BaseModel):
    total_tables: int
    total_columns: int
    indexed_tables: int
    indexed_columns: int
    last_indexed: datetime | None
    status: Literal["idle", "indexing", "error"]
```

## Security Considerations
- OpenAI API key from environment variable
- Admin-only access to index management
- Rate limiting on search endpoint

## Performance Requirements
- Search response < 500ms for top 10 results
- Embedding generation < 100ms per item
- Index rebuild < 5 minutes for 10k items

---
*Created: 2026-02-05*
*Status: Draft*
