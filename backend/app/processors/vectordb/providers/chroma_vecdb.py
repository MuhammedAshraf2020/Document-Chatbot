import logging
import os
from typing import List

from chromadb import Client, PersistentClient

from ..models import RetrievedDocument
from ..providers.base import BaseVectorDB


class ChromaVectorDB(BaseVectorDB):
    def __init__(self, db_path: str, metadata_fields: list = None):
        self.db_path = db_path
        self.metadata_fields = metadata_fields or []
        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = PersistentClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exist(self, collection_name: str) -> bool:
        try:
            self.client.get_collection(collection_name)
            return True
        except Exception:
            return False

    def list_all_collections(self) -> List[str]:
        collections = self.client.list_collections()
        return [collection.name for collection in collections]

    def get_collection_info(self, collection_name: str) -> dict:
        collection = self.client.get_collection(collection_name)
        return {"name": collection.name, "size": len(collection)}

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
                name=collection_name,
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
            collection = self.client.get_collection(collection_name)
            collection.add(
                documents=[text],
                embeddings=[vector],
                ids=[record_id],
                metadatas=[metadata],
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

        try:
            collection = self.client.get_collection(collection_name)
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i : i + batch_size]
                batch_vectors = vectors[i : i + batch_size]
                batch_metadata = metadata[i : i + batch_size]
                batch_record_ids = record_ids[i : i + batch_size]

                collection.add(
                    documents=batch_texts,
                    embeddings=batch_vectors,
                    ids=[str(i) for i in batch_record_ids],
                    metadatas=batch_metadata,
                )
        except Exception as e:
            self.logger.error(f"Error while inserting batch: {e}")
            return False

        return True

    def search_by_vector(
        self, collection_name: str, vector: list, limit: int = 5
    ) -> List[RetrievedDocument]:
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.query(query_embeddings=[vector], n_results=limit)

            # Modify to access results directly as text since 'result' is a string
            return [
                RetrievedDocument(score=1 - distance, text=document)
                for distance, document in zip(
                    results["distances"][0], results["documents"][0]
                )
            ]
        except Exception as e:
            self.logger.error(f"Error while searching: {e}")
            return []
