from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    VECTOR_DB_PATH: str = ""
    VECTOR_DB_TYPE: str = ""
    CHROMA_METADATA: str = ""

    EMBEDDER_TYPE: str = ""
    EMBEDDER_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = ""
    EMBEDDER_MODEL_ID: str = ""
    VECTOR_DB_DISTANCE_METHOD: str = "cosine"

    MODEL_ID: str = ""
    GENERATOR_TYPE: str = ""
    GENERATOR_API_KEY: str = ""

    MAX_OUTPUT_TOKENS: int = 1024
    TEMPERATURE: float = 0.7

    UPLOAD_DIR: Path = Path("uploads")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf"]
    PDF_STORING_PATH: Path = Path("pdf_store")

    class Config:
        env_file: str = ".env"


def get_settings():
    return Settings()
