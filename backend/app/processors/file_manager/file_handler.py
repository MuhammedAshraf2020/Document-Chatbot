from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple
from uuid import uuid4

import aiofiles
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class FileMetadata(BaseModel):
    """Data class for file metadata."""

    filename: str
    filepath: Path
    experiment_id: str
    size: int
    content_type: str


class FileValidationError(Exception):
    """Custom exception for file validation errors."""

    pass


class FileHandler:
    """Handles file operations with improved error handling and type safety."""

    def __init__(self, settings: BaseSettings):
        self.settings = settings
        self.base_dir = Path(__file__).parent.parent.parent
        self.upload_dir = self.base_dir / self.settings.UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def validate_file(self, file: UploadFile) -> None:
        """
        Validates file type and size.
        Raises FileValidationError if validation fails.
        """
        if file.content_type not in self.settings.ALLOWED_FILE_TYPES:
            raise FileValidationError(
                f"Invalid file type. Allowed types: {', '.join(self.settings.ALLOWED_FILE_TYPES)}"
            )

        # Get file size without reading entire file into memory
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > self.settings.MAX_FILE_SIZE:
            raise FileValidationError(
                f"File exceeds max size of {self.settings.MAX_FILE_SIZE / (1024 * 1024):.2f} MB"
            )

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generates a unique filename while preserving the extension."""
        stem = Path(original_filename).stem.lower().replace(" ", "_")
        suffix = Path(original_filename).suffix.lower()
        return f"{stem}_{uuid4().hex}{suffix}"

    async def save_file(self, file: UploadFile, experiment_id: str) -> FileMetadata:
        """
        Saves uploaded file and returns metadata.
        Raises HTTPException for errors.
        """
        try:
            await self.validate_file(file)

            experiment_path = self.upload_dir / str(experiment_id)
            experiment_path.mkdir(parents=True, exist_ok=True)

            unique_filename = self._generate_unique_filename(file.filename)
            file_path = experiment_path / unique_filename

            # Save file in chunks to handle large files
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(8192):  # 8KB chunks
                    await f.write(chunk)

            return FileMetadata(
                filename=unique_filename,
                filepath=file_path,
                experiment_id=experiment_id,
                size=file_path.stat().st_size,
                content_type=file.content_type,
            )

        except FileValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
