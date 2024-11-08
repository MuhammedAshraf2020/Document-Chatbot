from abc import ABC, abstractmethod
from typing import List, Optional, Union

import numpy as np


class EmbeddingBase(ABC):
    """Base abstract class for embedders."""

    @abstractmethod
    def __init__(
        self, api_key: Optional[str] = None, embedding_model_id: str = None, **kwargs
    ):
        """Initialize the embedder."""
        pass

    @abstractmethod
    def embed_text(self, chunks: List[str]) -> List[List[float]]:
        """
        Embed the given text chunks into vectors.

        Args:
            chunks: List of text strings to embed

        Returns:
            List of embedding vectors or numpy array
        """
        pass
