"""Search router for semantic search endpoints."""

from typing import Annotated
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.dependencies import get_db, require_admin
from src.models.db_models import Column, DataSource, Table
from src.models.schemas import User
from src.models.search_schemas import (
    IndexRebuildRequest,
    IndexRebuildResponse,
    IndexStatus,
    SearchRequest,
    SearchResponse,
    SearchResultItem,
)
from src.services.embedding import embedding_service
from src.services.vector_store import vector_store_service

router = APIRouter(prefix="/search", tags=["search"])
logger = structlog.get_logger(__name__)


@router.post("", response_model=SearchResponse)
async def semantic_search(
    request: SearchRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SearchResponse:
    """
    Perform semantic search over catalog metadata.

    Returns tables and columns matching the query.
    """
    # Check if embedding service is available
    if not embedding_service.is_available:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Embedding service is not configured. Set OPENAI_API_KEY.",
        )

    logger.info("semantic_search", query=request.query, limit=request.limit)

    try:
        # Generate query embedding
        query_embedding = await embedding_service.generate_embedding(request.query)

        # Build filter
        where_filter = None
        if request.data_source_id:
            where_filter = {"data_source_id": str(request.data_source_id)}

        if not request.include_columns:
            if where_filter:
                where_filter["type"] = "table"
            else:
                where_filter = {"type": "table"}

        # Search vector store
        results = vector_store_service.search(
            query_embedding=query_embedding,
            n_results=request.limit,
            where=where_filter,
        )

        # Convert results
        items: list[SearchResultItem] = []

        if results and results.get("ids") and results["ids"][0]:
            ids = results["ids"][0]
            distances = results.get("distances", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]

            for i, doc_id in enumerate(ids):
                metadata = metadatas[i] if i < len(metadatas) else {}
                distance = distances[i] if i < len(distances) else 1.0

                # Convert distance to similarity (cosine distance to similarity)
                similarity = 1 - distance

                items.append(
                    SearchResultItem(
                        id=UUID(doc_id),
                        type=metadata.get("type", "table"),
                        name=metadata.get("name", ""),
                        description=metadata.get("description"),
                        similarity_score=round(similarity, 4),
                        data_source_id=UUID(metadata.get("data_source_id", doc_id)),
                        data_source_name=metadata.get("data_source_name", "Unknown"),
                        table_name=metadata.get("table_name"),
                        schema_name=metadata.get("schema_name"),
                    )
                )

        return SearchResponse(
            results=items,
            total=len(items),
            query=request.query,
        )

    except Exception as e:
        logger.error("search_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


@router.post("/index/rebuild", response_model=IndexRebuildResponse)
async def rebuild_index(
    request: IndexRebuildRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)],
) -> IndexRebuildResponse:
    """
    Rebuild the vector index from database.

    Requires admin role.
    """
    # Check if embedding service is available
    if not embedding_service.is_available:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Embedding service is not configured. Set OPENAI_API_KEY.",
        )

    logger.info("rebuilding_index", user=current_user.email, force=request.force)

    try:
        # Clear existing index if force
        if request.force:
            vector_store_service.clear_collection()

        # Fetch all tables with their data sources
        tables_stmt = select(Table).options(selectinload(Table.data_source))
        tables_result = await db.execute(tables_stmt)
        tables = list(tables_result.scalars().all())

        # Fetch all columns with their tables
        columns_stmt = select(Column).options(
            selectinload(Column.table).selectinload(Table.data_source)
        )
        columns_result = await db.execute(columns_stmt)
        columns = list(columns_result.scalars().all())

        total_items = len(tables) + len(columns)

        if total_items == 0:
            return IndexRebuildResponse(
                status="completed",
                message="No items to index",
                estimated_items=0,
            )

        # Prepare table documents
        table_docs = []
        table_ids = []
        table_metadatas = []

        for table in tables:
            doc_text = f"{table.name}"
            if table.description:
                doc_text += f": {table.description}"
            if table.schema_name:
                doc_text = f"{table.schema_name}.{doc_text}"

            table_docs.append(doc_text)
            table_ids.append(str(table.id))
            table_metadatas.append({
                "type": "table",
                "name": table.name,
                "description": table.description or "",
                "schema_name": table.schema_name or "",
                "data_source_id": str(table.data_source_id),
                "data_source_name": table.data_source.name if table.data_source else "Unknown",
            })

        # Prepare column documents
        column_docs = []
        column_ids = []
        column_metadatas = []

        for column in columns:
            doc_text = f"{column.name} ({column.data_type})"
            if column.description:
                doc_text += f": {column.description}"

            column_docs.append(doc_text)
            column_ids.append(str(column.id))

            table = column.table
            column_metadatas.append({
                "type": "column",
                "name": column.name,
                "description": column.description or "",
                "data_type": column.data_type,
                "table_name": table.name if table else "",
                "schema_name": table.schema_name if table else "",
                "data_source_id": str(table.data_source_id) if table else "",
                "data_source_name": table.data_source.name if table and table.data_source else "Unknown",
            })

        # Generate embeddings for tables
        if table_docs:
            logger.info("generating_table_embeddings", count=len(table_docs))
            table_embeddings = await embedding_service.generate_embeddings_batch(table_docs)

            # Add to vector store
            vector_store_service.add_documents(
                ids=table_ids,
                embeddings=table_embeddings,
                documents=table_docs,
                metadatas=table_metadatas,
            )

        # Generate embeddings for columns
        if column_docs:
            logger.info("generating_column_embeddings", count=len(column_docs))
            column_embeddings = await embedding_service.generate_embeddings_batch(column_docs)

            # Add to vector store
            vector_store_service.add_documents(
                ids=column_ids,
                embeddings=column_embeddings,
                documents=column_docs,
                metadatas=column_metadatas,
            )

        logger.info("index_rebuild_complete", tables=len(tables), columns=len(columns))

        return IndexRebuildResponse(
            status="completed",
            message=f"Indexed {len(tables)} tables and {len(columns)} columns",
            estimated_items=total_items,
        )

    except Exception as e:
        logger.error("index_rebuild_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Index rebuild failed: {str(e)}",
        )


@router.get("/index/status", response_model=IndexStatus)
async def get_index_status(
    current_user: Annotated[User, Depends(require_admin)],
) -> IndexStatus:
    """
    Get the current status of the vector index.

    Requires admin role.
    """
    try:
        stats = vector_store_service.get_stats()

        return IndexStatus(
            total_documents=stats.get("total_documents", 0),
            indexed_tables=stats.get("tables", 0),
            indexed_columns=stats.get("columns", 0),
            last_indexed=None,  # Would need to track this separately
            status="idle",
            embedding_service_available=embedding_service.is_available,
            vector_store_available=vector_store_service.check_health(),
        )

    except Exception as e:
        logger.error("get_index_status_failed", error=str(e))
        return IndexStatus(
            total_documents=0,
            indexed_tables=0,
            indexed_columns=0,
            last_indexed=None,
            status="error",
            embedding_service_available=embedding_service.is_available,
            vector_store_available=False,
        )
