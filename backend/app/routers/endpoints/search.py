import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.utils.prompts import RAG_PROMPT

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/search", tags=["search"])


@router.post("/answer/{experiment_id}/{question}")
async def answer(
    experiment_id: str,
    question: str,
    request: Request,
) -> JSONResponse:
    """
    Endpoint to find relevant chunks for a given query and file.
    """
    try:
        settings = request.app.state.settings
        vector_db = request.app.vector_db
        embedder = request.app.embedder
        generator = request.app.generator

        # Generate embedding for the question
        question_embedding = embedder.embed_text([question])
        if not question_embedding:
            raise ValueError("Failed to generate question embedding.")

        # Search for relevant documents in the vector database
        most_relevant_docs = vector_db.search_by_vector(
            collection_name=f"collection_{experiment_id}",
            vector=question_embedding[0],
            limit=2,
        )
        if not most_relevant_docs:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        # Format prompt and generate answer
        prompt = RAG_PROMPT.format(
            question=question, chunks=[doc.text for doc in most_relevant_docs]
        )
        answer = generator.generate_text(
            prompt=prompt,
            chat_history=[],
            max_output_tokens=settings.MAX_OUTPUT_TOKENS,
            temperature=settings.TEMPERATURE,
        )

        return JSONResponse(content={"answer": answer})

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the request."
        )
