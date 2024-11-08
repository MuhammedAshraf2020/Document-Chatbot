import logging
from typing import List, Optional, Union

import numpy as np

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Please install the openai package")

from .base import EmbeddingBase
from .config import EmbedderConfig
from .exceptions import (
    ClientNotInitializedException,
    EmbeddingException,
    ModelNotSetException,
)


class OpenAIEmbedder(EmbeddingBase):
    """OpenAI implementation of embedder."""

    def __init__(
        self, api_key: str, embedding_model_id: str = "text-embedding-3-small", **kwargs
    ):
        self.config = EmbedderConfig(
            api_key=api_key, embedding_model_id=embedding_model_id, extra_params=kwargs
        )

        self.client = None
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        """Initialize the OpenAI client."""
        try:
            self.client = OpenAI(api_key=self.config.api_key)
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise ClientNotInitializedException(
                f"Failed to initialize OpenAI client: {str(e)}"
            )

    def embed_text(self, chunks: List[str]) -> Union[List[List[float]], np.ndarray]:
        """Generate embeddings for the given text chunks."""
        if not self.client:
            raise ClientNotInitializedException("OpenAI client is not connected")

        try:
            response = self.client.embeddings.create(
                model=self.config.embedding_model_id, input=chunks
            )

            embeddings = [item.embedding for item in response.data]
            return np.array(embeddings)

        except Exception as e:
            self.logger.error(f"Error generating embeddings with OpenAI: {str(e)}")
            raise EmbeddingException(f"Failed to generate embeddings: {str(e)}")
