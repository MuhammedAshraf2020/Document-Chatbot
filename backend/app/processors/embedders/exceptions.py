class EmbedderException(Exception):
    """Base exception for embedders."""

    pass


class ClientNotInitializedException(EmbedderException):
    """Raised when the client is not properly initialized."""

    pass


class ModelNotSetException(EmbedderException):
    """Raised when the embedding model is not set."""

    pass


class EmbeddingException(EmbedderException):
    """Raised when embedding generation fails."""

    pass
