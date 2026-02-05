# FEAT-003: Vector Store Integration - Technical Design

## Overview
ChromaDB vector store integration with OpenAI embeddings for semantic search over catalog metadata.

## Architecture

### System Context
```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                     API Layer                          │ │
│  │  /search  │  /index/rebuild  │  /index/status         │ │
│  └─────────────────────┬──────────────────────────────────┘ │
│                        │                                    │
│  ┌─────────────────────▼──────────────────────────────────┐ │
│  │                   Services                             │ │
│  │  EmbeddingService  │  VectorStoreService              │ │
│  └─────────────────────┬──────────────────────────────────┘ │
│                        │                                    │
└────────────────────────┼────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼────┐                    ┌────▼────┐
    │ OpenAI  │                    │ChromaDB │
    │   API   │                    │(Local)  │
    └─────────┘                    └─────────┘
```

### Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| EmbeddingService | Generate embeddings via OpenAI | `src/services/embedding.py` |
| VectorStoreService | ChromaDB operations | `src/services/vector_store.py` |
| SearchRouter | Search API endpoints | `src/api/routers/search.py` |
| Search Schemas | Request/Response models | `src/models/search_schemas.py` |

## Data Flow

### Search Flow
```
1. User sends POST /api/v1/search with query
2. SearchRouter receives request
3. EmbeddingService generates query embedding
4. VectorStoreService queries ChromaDB
5. Results ranked by similarity score
6. Response returned to user
```

### Index Rebuild Flow
```
1. Admin calls POST /api/v1/index/rebuild
2. Fetch all tables/columns from database
3. Generate embeddings in batches (100 items)
4. Upsert to ChromaDB
5. Update index status
```

## File Structure

### New Files
```
src/
├── services/
│   ├── __init__.py
│   ├── embedding.py         # OpenAI embedding service
│   └── vector_store.py      # ChromaDB service
├── api/routers/
│   └── search.py            # Search endpoints
├── models/
│   └── search_schemas.py    # Search Pydantic models

chroma_data/                  # ChromaDB persistence (gitignored)
```

### Modified Files
```
src/core/config.py           # Add OpenAI/ChromaDB settings
src/api/main.py              # Add search router
.env.example                 # Add OPENAI_API_KEY
pyproject.toml               # Add chromadb, openai deps
.gitignore                   # Add chroma_data/
```

## API Design

### POST /api/v1/search
```json
// Request
{
  "query": "customer orders",
  "limit": 10,
  "data_source_id": "uuid-optional",
  "include_columns": true
}

// Response
{
  "results": [
    {
      "id": "uuid",
      "type": "table",
      "name": "orders",
      "description": "Customer order transactions",
      "similarity_score": 0.92,
      "data_source_name": "production_db",
      "table_name": null
    },
    {
      "id": "uuid",
      "type": "column",
      "name": "customer_id",
      "description": "Foreign key to customers",
      "similarity_score": 0.87,
      "data_source_name": "production_db",
      "table_name": "orders"
    }
  ],
  "total": 2,
  "query": "customer orders"
}
```

### POST /api/v1/index/rebuild
```json
// Response
{
  "status": "started",
  "message": "Index rebuild initiated",
  "estimated_items": 150
}
```

### GET /api/v1/index/status
```json
{
  "total_tables": 50,
  "total_columns": 500,
  "indexed_tables": 50,
  "indexed_columns": 500,
  "last_indexed": "2026-02-05T10:30:00Z",
  "status": "idle"
}
```

## Service Implementation

### EmbeddingService
```python
class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model

    async def generate_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    async def generate_batch(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [d.embedding for d in response.data]
```

### VectorStoreService
```python
class VectorStoreService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.collection = self.client.get_or_create_collection("catalog")

    def add_documents(self, ids, embeddings, metadatas, documents):
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def search(self, embedding, n_results=10, where=None):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            where=where
        )
```

## Configuration

### Environment Variables
```bash
# OpenAI
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_data
```

## Implementation Order
1. Add dependencies (openai, chromadb)
2. Update config with new settings
3. Create EmbeddingService
4. Create VectorStoreService
5. Create search schemas
6. Create search router
7. Update main.py to include router
8. Update .gitignore
9. Create tests

---
*Generated: 2026-02-05*
*Status: Ready for implementation*
