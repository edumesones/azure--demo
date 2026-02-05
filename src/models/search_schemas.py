"""Pydantic schemas for search API."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request model for semantic search."""

    query: str = Field(..., min_length=1, max_length=500, description="Search query text")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results to return")
    data_source_id: UUID | None = Field(default=None, description="Filter by data source")
    include_columns: bool = Field(default=True, description="Include column results")


class SearchResultItem(BaseModel):
    """Single search result item."""

    id: UUID
    type: Literal["table", "column"]
    name: str
    description: str | None
    similarity_score: float = Field(..., ge=0, le=1)
    data_source_id: UUID
    data_source_name: str
    table_name: str | None = None  # Only for columns
    schema_name: str | None = None


class SearchResponse(BaseModel):
    """Response model for semantic search."""

    results: list[SearchResultItem]
    total: int
    query: str


class IndexRebuildRequest(BaseModel):
    """Request model for index rebuild."""

    force: bool = Field(default=False, description="Force rebuild even if index exists")


class IndexRebuildResponse(BaseModel):
    """Response model for index rebuild."""

    status: Literal["started", "completed", "error"]
    message: str
    estimated_items: int = 0


class IndexStatus(BaseModel):
    """Status of the vector index."""

    total_documents: int
    indexed_tables: int
    indexed_columns: int
    last_indexed: datetime | None = None
    status: Literal["idle", "indexing", "error"]
    embedding_service_available: bool
    vector_store_available: bool
