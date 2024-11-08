from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class FileProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    async def generate_chunks(self, file_path: str) -> List[str]:
        if not file_path.endswith(".pdf"):
            raise ValueError("Unsupported file type. Only PDF files are allowed.")

        loader = PyPDFLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.create_documents(
            [doc.page_content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
        )
        list_of_chunks = [chunk.page_content for chunk in chunks]
        return list_of_chunks
