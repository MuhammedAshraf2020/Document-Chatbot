from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class RetrievedDocument:
    score: float
    text: str


class VectorDBConfig(BaseModel):
    vector_db_path: str
    faiss_index_path: str
    chroma_db_path: str
    chroma_metadata_fields: list
    vector_db_distance_method: str
