from enum import Enum


class VectorDBType(Enum):
    QDRANT = "qdrant"
    MILVUS = "milvus"
    FAISS = "faiss"
    CHROMA = "chroma"


class DistanceMethod(Enum):
    COSINE = "cosine"
    DOT = "dot"
