import os

from .enums import VectorDBType
from .providers import BaseVectorDB


class VectorDBFactory:

    @staticmethod
    def create(
        vector_db_type: str,
        db_path: str,
    ) -> BaseVectorDB:
        db_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__),
                )
            ),
            db_path,
        )
        if vector_db_type == VectorDBType.QDRANT.value:
            from .providers import QdrantVectorDB

            return QdrantVectorDB(
                db_path=db_path,
            )
        elif vector_db_type == VectorDBType.CHROMA.value:
            from .providers import ChromaVectorDB

            return ChromaVectorDB(
                db_path=db_path,
            )
        else:
            raise ValueError(f"Invalid vector DB provider type: {vector_db_type}")
