"""OpenAI embedding service for generating text embeddings."""

import asyncio
from functools import lru_cache

import structlog
from openai import AsyncOpenAI

from src.core.config import settings

logger = structlog.get_logger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using OpenAI."""

    def __init__(self) -> None:
        """Initialize the embedding service."""
        self._client: AsyncOpenAI | None = None
        self._model = settings.embedding_model

    @property
    def client(self) -> AsyncOpenAI:
        """Get or create the OpenAI client."""
        if self._client is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not configured")
            self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        return self._client

    @property
    def is_available(self) -> bool:
        """Check if embedding service is available."""
        return settings.openai_api_key is not None

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to generate embedding for

        Returns:
            List of floats representing the embedding vector
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")

        logger.debug("generating_embedding", text_length=len(text))

        response = await self.client.embeddings.create(
            model=self._model,
            input=text,
        )

        return response.data[0].embedding

    async def generate_embeddings_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts in batches.

        Args:
            texts: List of texts to generate embeddings for
            batch_size: Number of texts to process per API call

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        # Filter empty texts and track indices
        valid_texts = []
        valid_indices = []
        for i, text in enumerate(texts):
            if text.strip():
                valid_texts.append(text)
                valid_indices.append(i)

        if not valid_texts:
            return [[] for _ in texts]

        logger.info(
            "generating_embeddings_batch",
            total_texts=len(texts),
            valid_texts=len(valid_texts),
            batch_size=batch_size,
        )

        all_embeddings: list[list[float]] = []

        # Process in batches
        for i in range(0, len(valid_texts), batch_size):
            batch = valid_texts[i : i + batch_size]
            logger.debug(
                "processing_batch",
                batch_number=i // batch_size + 1,
                batch_size=len(batch),
            )

            response = await self.client.embeddings.create(
                model=self._model,
                input=batch,
            )

            batch_embeddings = [d.embedding for d in response.data]
            all_embeddings.extend(batch_embeddings)

        # Reconstruct full list with empty embeddings for invalid texts
        result: list[list[float]] = [[] for _ in texts]
        for idx, embedding in zip(valid_indices, all_embeddings):
            result[idx] = embedding

        return result

    async def check_health(self) -> bool:
        """
        Check if the embedding service is healthy.

        Returns:
            True if service is available and working
        """
        if not self.is_available:
            return False

        try:
            # Generate a test embedding
            await self.generate_embedding("health check")
            return True
        except Exception as e:
            logger.error("embedding_health_check_failed", error=str(e))
            return False


@lru_cache
def get_embedding_service() -> EmbeddingService:
    """Get cached embedding service instance."""
    return EmbeddingService()


# Singleton instance
embedding_service = get_embedding_service()
