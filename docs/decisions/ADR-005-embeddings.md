# ADR-005: Use OpenAI text-embedding-3-small for Embeddings

## Status
Accepted

## Date
2026-02-05

## Context
We need an embedding model to convert metadata documents into vectors for semantic search.

Requirements:
- High quality semantic representations
- Cost-effective for demo/development
- Easy integration with LangChain
- Configurable for Azure OpenAI

## Options Considered

### Option 1: OpenAI text-embedding-3-small
**Pros:**
- Excellent quality-to-cost ratio
- 1536 dimensions (good balance)
- Easy API integration
- $0.02 per 1M tokens
- JD alignment (OpenAI/Azure OpenAI)

**Cons:**
- API dependency
- Network latency

### Option 2: OpenAI text-embedding-3-large
**Pros:**
- Higher quality
- 3072 dimensions

**Cons:**
- 5x more expensive
- Overkill for metadata search

### Option 3: sentence-transformers (local)
**Pros:**
- Free, runs locally
- No API dependency

**Cons:**
- Lower quality for specialized domains
- Requires GPU for performance
- More setup complexity

### Option 4: Azure OpenAI Embeddings
**Pros:**
- Enterprise compliance
- Same models as OpenAI

**Cons:**
- More setup (Azure subscription)
- Similar cost

## Decision
**OpenAI text-embedding-3-small** with configurable backend for Azure OpenAI.

## Consequences
- Configure embedding model via environment variables
- Support both OpenAI and Azure OpenAI endpoints
- Mock embeddings in tests to avoid API costs
- Cache embeddings to reduce API calls

## Configuration
```python
# .env
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_PROVIDER=openai  # or azure_openai
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
```
