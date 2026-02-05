"""ChromaDB vector store service for semantic search."""

import asyncio
from functools import lru_cache
from pathlib import Path
from typing import Any
from uuid import UUID

import chromadb
import structlog
from chromadb.config import Settings as ChromaSettings

from src.core.config import settings

logger = structlog.get_logger(__name__)


class VectorStoreService:
    """Service for ChromaDB vector store operations."""

    def __init__(self) -> None:
        """Initialize the vector store service."""
        self._client: chromadb.ClientAPI | None = None
        self._collection: chromadb.Collection | None = None

    def _ensure_persist_dir(self) -> None:
        """Ensure the persistence directory exists."""
        persist_dir = Path(settings.chroma_persist_dir)
        persist_dir.mkdir(parents=True, exist_ok=True)

    @property
    def client(self) -> chromadb.ClientAPI:
        """Get or create the ChromaDB client."""
        if self._client is None:
            self._ensure_persist_dir()
            self._client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                ),
            )
        return self._client

    @property
    def collection(self) -> chromadb.Collection:
        """Get or create the catalog collection."""
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=settings.chroma_collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def add_documents(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """
        Add or update documents in the vector store.

        Args:
            ids: Unique identifiers for documents
            embeddings: Embedding vectors
            documents: Original text documents
            metadatas: Metadata for each document
        """
        if not ids:
            return

        logger.info("adding_documents", count=len(ids))

        # ChromaDB upsert handles both insert and update
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 10,
        where: dict[str, Any] | None = None,
        where_document: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Search for similar documents.

        Args:
            query_embedding: Query vector
            n_results: Maximum number of results
            where: Metadata filter
            where_document: Document content filter

        Returns:
            Search results with ids, distances, documents, and metadatas
        """
        logger.debug("searching", n_results=n_results, has_filter=where is not None)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=["documents", "metadatas", "distances"],
        )

        return results

    def delete_documents(self, ids: list[str]) -> None:
        """
        Delete documents from the vector store.

        Args:
            ids: Document IDs to delete
        """
        if not ids:
            return

        logger.info("deleting_documents", count=len(ids))
        self.collection.delete(ids=ids)

    def get_count(self) -> int:
        """Get the total number of documents in the collection."""
        return self.collection.count()

    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        logger.warning("clearing_collection")
        # Delete and recreate collection
        self.client.delete_collection(settings.chroma_collection_name)
        self._collection = None
        # Recreate
        _ = self.collection

    def get_stats(self) -> dict[str, Any]:
        """
        Get collection statistics.

        Returns:
            Dictionary with collection stats
        """
        count = self.get_count()

        # Get type breakdown from metadata
        tables_count = 0
        columns_count = 0

        if count > 0:
            # Sample to get type distribution
            try:
                # Get all with type metadata
                results = self.collection.get(
                    include=["metadatas"],
                    limit=count,
                )
                if results and results.get("metadatas"):
                    for meta in results["metadatas"]:
                        if meta and meta.get("type") == "table":
                            tables_count += 1
                        elif meta and meta.get("type") == "column":
                            columns_count += 1
            except Exception as e:
                logger.warning("failed_to_get_type_stats", error=str(e))

        return {
            "total_documents": count,
            "tables": tables_count,
            "columns": columns_count,
        }

    def check_health(self) -> bool:
        """
        Check if vector store is healthy.

        Returns:
            True if service is available
        """
        try:
            _ = self.collection.count()
            return True
        except Exception as e:
            logger.error("vector_store_health_check_failed", error=str(e))
            return False


@lru_cache
def get_vector_store_service() -> VectorStoreService:
    """Get cached vector store service instance."""
    return VectorStoreService()


# Singleton instance
vector_store_service = get_vector_store_service()
