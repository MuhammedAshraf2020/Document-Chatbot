import json
import logging
import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.processors.file_manager import FileHandler, FileProcessor

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload/{experiment_id}")
async def upload_file(
    experiment_id: str,
    file: UploadFile,
    request: Request,
) -> JSONResponse:
    """Upload and validate a file."""
    try:
        file_handler = FileHandler(settings=get_settings())
        metadata = await file_handler.save_file(file=file, experiment_id=experiment_id)
        file_path = metadata.filepath

        if not file_path.exists():
            return JSONResponse(status_code=404, content={"error": "File not found"})

        processor = FileProcessor()
        chunks = await processor.generate_chunks(str(file_path))
        embeddings = request.app.embedder.embed_text(chunks=chunks)

        # Create and populate vector database collection
        vector_db = request.app.vector_db
        collection_name = f"collection_{experiment_id}"

        vector_db.create_collection(
            collection_name=collection_name,
            embedding_size=len(embeddings[0]),
            distance_method=request.app.state.settings.VECTOR_DB_DISTANCE_METHOD,
        )

        vector_db.insert_many(
            collection_name=collection_name,
            texts=chunks,
            vectors=embeddings,
            record_ids=[str(uuid4()) for _ in range(len(chunks))],
        )

        return JSONResponse(
            status_code=200, content={"embeddings_count": len(embeddings)}
        )

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
