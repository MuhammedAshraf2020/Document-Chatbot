from enum import Enum
from typing import Optional

from .base import EmbeddingBase


class EmbedderType(Enum):
    COHERE = "COHERE"
    OPENAI = "OPENAI"
    SENTENCE_TRANSFORMER = "SENTENCE_TRANSFORMER"


class EmbedderFactory:
    """Factory class for creating embedders."""

    DEFAULT_MODELS = {
        EmbedderType.COHERE.value: "embed-english-v3.0",
        EmbedderType.OPENAI.value: "text-embedding-3-small",
        EmbedderType.SENTENCE_TRANSFORMER.value: "all-MiniLM-L6-v2",
    }

    @staticmethod
    def create_embedder(
        embedder_type: EmbedderType,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ) -> EmbeddingBase:
        """Create an embedder instance based on the specified type."""

        if embedder_type == EmbedderType.COHERE.value:
            from .cohere_embedder import CohereEmbedder

            embedder_class = CohereEmbedder
        elif embedder_type == EmbedderType.OPENAI.value:
            from .openai_embedder import OpenAIEmbedder

            embedder_class = OpenAIEmbedder
        elif embedder_type == EmbedderType.SENTENCE_TRANSFORMER.value:
            from .sentence_transformer_embedder import SentenceTransformerEmbedder

            embedder_class = SentenceTransformerEmbedder
        else:
            raise ValueError(f"Unsupported embedder type: {embedder_type}")

        # Use default model if none provided
        if not model_id:
            model_id = EmbedderFactory.DEFAULT_MODELS[embedder_type]

        # SentenceTransformer doesn't need an API key
        if embedder_type == EmbedderType.SENTENCE_TRANSFORMER:
            return embedder_class(embedding_model_id=model_id, **kwargs)

        # Other embedders need an API key
        if not api_key:
            raise ValueError(f"API key is required for {embedder_type.value}")

        return embedder_class(api_key=api_key, embedding_model_id=model_id, **kwargs)
