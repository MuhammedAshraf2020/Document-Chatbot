# embedders/sentence_transformer_embedder.py
import logging
from typing import List, Optional, Union

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    raise ImportError("Please install the sentence-transformers package")

from .base import EmbeddingBase
from .config import EmbedderConfig
from .exceptions import ClientNotInitializedException, EmbeddingException


class SentenceTransformerEmbedder(EmbeddingBase):
    """Sentence Transformer implementation of embedder."""

    def __init__(self, embedding_model_id: str = "all-MiniLM-L6-v2", **kwargs):
        self.config = EmbedderConfig(
            api_key=None,  # Not needed for Sentence Transformers
            embedding_model_id=embedding_model_id,
            extra_params=kwargs,
        )

        self.model = None
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        """Initialize the Sentence Transformer model."""
        try:
            self.model = SentenceTransformer(self.config.embedding_model_id)
        except Exception as e:
            self.logger.error(
                f"Failed to initialize Sentence Transformer model: {str(e)}"
            )
            raise ClientNotInitializedException(
                f"Failed to initialize Sentence Transformer model: {str(e)}"
            )

    def embed_text(self, chunks: List[str]) -> List[List[float]]:
        """Generate embeddings for the given text chunks."""
        if not self.model:
            raise ClientNotInitializedException(
                "Sentence Transformer model is not initialized"
            )

        try:
            embeddings = self.model.encode(
                chunks, convert_to_numpy=True, show_progress_bar=False
            ).tolist()
            return embeddings

        except Exception as e:
            self.logger.error(
                f"Error generating embeddings with Sentence Transformers: {str(e)}"
            )
            raise EmbeddingException(f"Failed to generate embeddings: {str(e)}")
