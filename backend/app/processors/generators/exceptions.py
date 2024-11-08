class TextGeneratorException(Exception):
    """Base exception for text generators."""

    pass


class ClientNotInitializedException(TextGeneratorException):
    """Raised when the client is not properly initialized."""

    pass


class ModelNotSetException(TextGeneratorException):
    """Raised when the generation model is not set."""

    pass


class GenerationException(TextGeneratorException):
    """Raised when text generation fails."""

    pass
