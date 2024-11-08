import logging
from typing import List

from qdrant_client import QdrantClient, models

from ..enums import DistanceMethod
from ..models import RetrievedDocument
from ..providers.base import BaseVectorDB


class QdrantVectorDB(BaseVectorDB):
    def __init__(self, db_path: str):
        self.client = None
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)

    def _get_distance_method(self, method: str):
        if method == DistanceMethod.COSINE.value:
            return models.Distance.COSINE
        elif method == DistanceMethod.DOT.value:
            return models.Distance.DOT
        else:
            raise ValueError(f"Invalid distance method: {method}")

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exist(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> List[str]:
        return [c.name for c in self.client.get_collections()]

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        if self.is_collection_exist(collection_name):
            self.client.delete_collection(collection_name=collection_name)

    def create_collection(
        self,
        collection_name: str,
        embedding_size: int,
        distance_method: str,
        reset: bool = False,
    ):
        if reset:
            self.delete_collection(collection_name)

        if not self.is_collection_exist(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, distance=distance_method
                ),
            )
            return True
        return False

    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ):
        if not self.is_collection_exist(collection_name):
            self.logger.error(
                f"Cannot insert record to non-existent collection: {collection_name}"
            )
            return False

        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=record_id,
                        vector=vector,
                        payload={"text": text, "metadata": metadata},
                    )
                ],
            )
        except Exception as e:
            self.logger.error(f"Error while inserting record: {e}")
            return False

        return True

    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50,
    ):
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            batch_vectors = vectors[i : i + batch_size]
            batch_metadata = metadata[i : i + batch_size]
            batch_record_ids = record_ids[i : i + batch_size]

            batch_records = [
                models.Record(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={"text": batch_texts[x], "metadata": batch_metadata[x]},
                )
                for x in range(len(batch_texts))
            ]

            try:
                self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False

        return True

    def search_by_vector(
        self, collection_name: str, vector: list, limit: int = 5
    ) -> List[RetrievedDocument]:
        results = self.client.search(
            collection_name=collection_name, query_vector=vector, limit=limit
        )

        if not results or len(results) == 0:
            return []

        return [
            RetrievedDocument(
                score=result.score,
                text=result.payload["text"],
            )
            for result in results
        ]
