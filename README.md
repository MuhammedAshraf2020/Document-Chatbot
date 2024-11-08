
# Document-Based Chatbot

This project is a document-based chatbot that leverages advanced NLP techniques to answer user queries based on knowledge extracted from PDF documents. The application provides an API and user interface that allows users to upload documents, process their contents, and interact with a chatbot that retrieves relevant information from the uploaded files.

## Project Overview

The chatbot is designed for the following tasks:
1. **Document Upload and Processing**: Users upload PDF files, and the application extracts and processes text to create a searchable knowledge base.
2. **Conversational Q&A**: The chatbot uses the processed knowledge base to answer questions, leveraging various AI models for embedding and text generation.
3. **User Interface**: A simple web interface enables document uploads and interactive chat with the chatbot.

## Features

- **Multiple Embedder Options**: Supports `Sentence-Transformer`, `Cohere`, and `OpenAI` for embedding text.
- **Vector Database Support**: Choose between `Chroma` and `Qdrant` vector databases for similarity search.
- **Text Generators**: Supports `GROQ`, `Mistral`, and `OpenAI GPT-4`.
- **Containerized Deployment**: Both frontend and backend are containerized using Docker for easy deployment.
- **API-Based Interaction**: Provides REST APIs for file upload and question-answering.

## Technologies

- **Backend**: FastAPI, Python
- **Frontend**: React with Material-UI
- **Vector Databases**: Chroma, Qdrant
- **Embedders**: Sentence-Transformer, Cohere, OpenAI
- **Text Generators**: GROQ, OpenAI GPT-4

## Project Structure

```
project-root/
├── docker-compose.yml              # Orchestrates frontend and backend containers
├── frontend/                       # React frontend
│   ├── Dockerfile                  # Dockerfile for the frontend
│   ├── src/                        # Source code for React
│   └── public/                     # Public assets for the React app
├── backend/                        # FastAPI backend
│   ├── Dockerfile                  # Dockerfile for the backend
│   ├── app/                        # Application code for FastAPI
│   ├── requirements.txt            # Backend dependencies
└── README.md                       # Project documentation
```

## Prerequisites

- **Docker** and **Docker Compose**
- **API Keys**: Obtain API keys for any external services (e.g., Cohere, OpenAI, GROQ) you are using.

## Getting Started

### 1. Environment Configuration

Create a `.env` file in the `backend` directory with the following content:

```ini
# Distance Method for Vector Database
VECTOR_DB_DISTANCE_METHOD="cosine"

# Vector Database Configuration
VECTOR_DB_TYPE="chroma"             # Options: chroma, qdrant
VECTOR_DB_PATH="db/"                # Path to the local vector database files
CHROMA_METADATA=""                  # Metadata path if using Chroma

# Embedder Configuration
EMBEDDER_TYPE="COHERE"              # Options: OPENAI, COHERE, SENTENCE_TRANSFORMER
EMBEDDER_API_KEY="cohere_api_key_here"
HUGGINGFACE_MODEL="sentence-transformers/all-mpnet-base-v2"  # For Sentence Transformer
EMBEDDER_MODEL_ID="embed-english-v3.0"

# Text Generator Configuration
GENERATOR_TYPE="GROQ"               # Options: GROQ, OPENAI
GENERATOR_API_KEY="groq_api_key_here"
MODEL_ID="mixtral-8x7b-32768"

# File Upload Settings
UPLOAD_DIR="uploads"
MAX_FILE_SIZE=10485760              # 10MB
ALLOWED_FILE_TYPES=["application/pdf"]
PDF_STORING_PATH="pdf_store"

# Chatbot Settings
MAX_OUTPUT_TOKENS=1000
TEMPERATURE=0.7
```

Replace the placeholders with actual API keys and model IDs.

### 2. Docker Setup

Use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

- The **frontend** will be available at `http://localhost:3000`.
- The **backend** API will be available at `http://localhost:8000`.

### 3. Frontend Usage

The frontend provides a user-friendly interface to:
- **Upload PDFs** to process and store information.
- **Ask questions** based on uploaded documents through a chat interface.

### 4. API Endpoints

The backend API allows for document upload and interactive question-answering.

#### Document Upload

`POST /files/upload/{experiment_id}`

- **Parameters**: `experiment_id` (string) - a unique identifier for the document set.
- **Body**: A PDF file to upload.
- **Response**: JSON response with a message confirming successful upload or an error.

#### Chat API

`POST /search/answer/{experiment_id}/{question}`

- **Parameters**: 
  - `experiment_id` (string) - the identifier used during document upload.
  - `question` (string) - the user’s question.
- **Response**: JSON response containing the chatbot's answer.

### Frontend Components

1. **File Upload**: Users enter an `experiment_id` and select PDF files to upload, creating a searchable knowledge base for each unique `experiment_id`.
2. **Chat Interface**: After uploading, users can ask multiple questions based on the knowledge extracted from the documents.

## Backend Details

The backend uses various AI/ML models for embeddings and text generation. The models and databases are configurable based on environment settings.

- **Embedders**:
  - `Sentence-Transformer` for local embeddings.
  - `Cohere` for cloud-based embeddings.
  - `OpenAI` for embeddings via the OpenAI API.
  
- **Vector Databases**:
  - **Chroma** and **Qdrant** are supported as vector databases to perform similarity search.

- **Text Generators**:
  - `GROQ Mistral`
  - `OpenAI GPT-4`

## Additional Configuration

### Vector Database Selection

Set `VECTOR_DB_TYPE` to `chroma` or `qdrant` in the `.env` file to specify which vector database to use. If `chroma` is chosen, `VECTOR_DB_PATH` should be a valid directory for local storage.

### Embedder and Text Generator Configuration

Configure the embedder and text generator types in `.env`:
- **EMBEDDER_TYPE** can be set to `SENTENCE_TRANSFORMER`, `COHERE`, or `OPENAI`.
- **GENERATOR_TYPE** can be set to `GROQ` or `OPENAI`.

For cloud-based embeddings or generation, ensure API keys are added in `.env`.

## Deployment

1. **Docker**: The application is containerized using Docker for easy deployment and environment consistency.
2. **Docker Compose**: Docker Compose is used to manage both frontend and backend containers, simplifying the deployment process.

## Example Commands

**Start Application**:
```bash
docker-compose up --build
```

**Stop Application**:
```bash
docker-compose down
```

## Future Enhancements

- **Authentication**: Adding user authentication for secure access.
- **Improved NLP Models**: Experiment with additional NLP models for better accuracy.
- **Additional File Formats**: Extend support for more document types beyond PDFs.
