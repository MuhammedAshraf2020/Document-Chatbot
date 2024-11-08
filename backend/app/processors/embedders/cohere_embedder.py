import logging
from typing import List, Optional, Union

try:
    import cohere
except ImportError:
    raise ImportError("Please install the cohere package")
import numpy as np

from .base import EmbeddingBase
from .config import EmbedderConfig
from .exceptions import ClientNotInitializedException, EmbeddingException


class CohereEmbedder(EmbeddingBase):
    """Cohere implementation of embedder."""

    def __init__(
        self, api_key: str, embedding_model_id: str = "embed-english-v3.0", **kwargs
    ):
        self.config = EmbedderConfig(
            api_key=api_key, embedding_model_id=embedding_model_id, extra_params=kwargs
        )

        self.client = None
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        """Initialize the Cohere client."""
        try:
            self.client = cohere.Client(api_key=self.config.api_key)
        except Exception as e:
            self.logger.error(f"Failed to initialize Cohere client: {str(e)}")
            raise ClientNotInitializedException(
                f"Failed to initialize Cohere client: {str(e)}"
            )

    def embed_text(self, chunks: List[str]) -> List[List[float]]:
        """Generate embeddings for the given text chunks."""
        if not self.client:
            raise ClientNotInitializedException("Cohere client is not connected")

        try:
            response = self.client.embed(
                model=self.config.embedding_model_id,
                texts=chunks,
                input_type="classification",
                embedding_types=["float"],
            )

            return np.array(response.embeddings.float).tolist()

        except Exception as e:
            self.logger.error(f"Error generating embeddings with Cohere: {str(e)}")
            raise EmbeddingException(f"Failed to generate embeddings: {str(e)}")
