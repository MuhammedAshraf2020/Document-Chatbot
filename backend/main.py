import logging
from contextlib import asynccontextmanager

from app.config import get_settings
from app.processors.embedders import EmbedderFactory
from app.processors.generators import TextGeneratorFactory
from app.processors.vectordb import VectorDBFactory
from app.routers import files_router, search_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application and logger
app = FastAPI()
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for FastAPI app lifespan to handle startup and shutdown tasks."""
    try:
        # Load settings and initialize components
        settings = get_settings()
        app.state.settings = settings

        # Initialize embedder
        app.embedder = EmbedderFactory.create_embedder(
            embedder_type=settings.EMBEDDER_TYPE,
            api_key=settings.EMBEDDER_API_KEY,
            model_id=settings.EMBEDDER_MODEL_ID,
        )
        logger.info("Embedder initialized successfully.")

        # Initialize vector database
        app.vector_db = VectorDBFactory.create(
            vector_db_type=settings.VECTOR_DB_TYPE,
            db_path=settings.VECTOR_DB_PATH,
        )
        app.vector_db.connect()
        logger.info("Vector database connected successfully.")

        # Initialize text generator
        app.generator = TextGeneratorFactory.create_generator(
            generator_type=settings.GENERATOR_TYPE,
            api_key=settings.GENERATOR_API_KEY,
            model_id=settings.MODEL_ID,
        )
        logger.info("Text generator initialized successfully.")

        yield  # Yield control to the app

    except Exception as e:
        logger.error(f"Error during app startup: {e}")
        raise e

    finally:
        # Shutdown tasks
        if hasattr(app, "vector_db"):
            app.vector_db.disconnect()
            logger.info("Vector database disconnected successfully.")


# Set lifespan context
app.router.lifespan_context = lifespan

# Include routers
app.include_router(search_router)
app.include_router(files_router)
