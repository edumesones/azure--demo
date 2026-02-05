# ADR-004: Use ChromaDB (dev) / Qdrant (prod) for Vector Storage

## Status
Accepted

## Date
2026-02-05

## Context
We need a vector database to store and search embedded metadata documents. Requirements:
- Store embeddings for semantic search
- Support hybrid search (vector + metadata filters)
- Easy local development
- Scalable for production

## Options Considered

### Option 1: ChromaDB
**Pros:**
- Simple setup (in-memory or persistent)
- Python-native
- Good for development and demos
- Built-in hybrid search

**Cons:**
- Not production-grade at scale
- Limited clustering support

### Option 2: Qdrant
**Pros:**
- Production-ready
- Excellent performance at scale
- Rich filtering capabilities
- Cloud and self-hosted options

**Cons:**
- More setup complexity
- Overkill for demo

### Option 3: Pinecone
**Pros:**
- Fully managed
- Excellent performance

**Cons:**
- Cloud-only (no local dev)
- Cost for demo usage
- Vendor lock-in

### Option 4: pgvector
**Pros:**
- PostgreSQL extension
- Single database for all data

**Cons:**
- Performance not optimized for vector search
- Limited hybrid search capabilities

## Decision
**ChromaDB for development/demo, Qdrant for production path** - Best balance of simplicity for demo with clear upgrade path.

## Consequences
- Abstract vector store behind interface for easy swapping
- Use ChromaDB persistent mode for demo
- Document Qdrant migration in architecture docs
- Configure via environment variables

## Interface Pattern
```python
class VectorStore(Protocol):
    async def add_documents(self, docs: list[Document]) -> None: ...
    async def search(self, query: str, k: int, filters: dict) -> list[Document]: ...
```
