# ADR-007: Use Azure Blob Storage for Dataset Files

## Status
Accepted

## Date
2026-02-05

## Context
We need storage for uploaded dataset files (CSV, Parquet, JSON). Requirements:
- Scalable file storage
- Support large files (100MB+)
- Azure cloud alignment (JD requirement)
- Cost-effective

## Options Considered

### Option 1: Azure Blob Storage
**Pros:**
- JD requirement alignment
- Scalable and cost-effective
- SDK well-documented
- Integrates with Azure ecosystem

**Cons:**
- Requires Azure subscription
- Network latency for local dev

### Option 2: AWS S3
**Pros:**
- Industry standard
- Excellent tooling

**Cons:**
- Not Azure (JD requirement)
- Different cloud ecosystem

### Option 3: Local filesystem
**Pros:**
- Simple for development
- No cloud dependency

**Cons:**
- Not scalable
- Not cloud-native
- No replication

### Option 4: MinIO (S3-compatible)
**Pros:**
- S3-compatible for local dev
- Can run in Docker

**Cons:**
- Additional infrastructure
- Not Azure-native

## Decision
**Azure Blob Storage** with local filesystem fallback for development.

## Consequences
- Use azure-storage-blob SDK
- Configure via environment variables
- Implement storage interface for testing with local filesystem
- Use SAS tokens for secure access

## Configuration
```python
# .env
STORAGE_PROVIDER=azure  # or local
AZURE_STORAGE_CONNECTION_STRING=...
AZURE_STORAGE_CONTAINER=datasets
LOCAL_STORAGE_PATH=./data/uploads
```

## Interface Pattern
```python
class StorageClient(Protocol):
    async def upload(self, filename: str, content: bytes) -> str: ...
    async def download(self, filename: str) -> bytes: ...
    async def delete(self, filename: str) -> None: ...
```
