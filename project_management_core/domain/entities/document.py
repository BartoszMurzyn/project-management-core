from datetime import datetime

from pydantic import BaseModel


class Document(BaseModel):
    """Domain entity representing an uploaded document and its metadata."""
    id: int | None = None
    original_filename: str
    generated_filename: str
    file_path: str
    file_size: int
    content_type: str
    project_id: int
    uploaded_by: int
    uploaded_at: datetime | None = None

    def get_metadata(self) -> dict:
        """Return a metadata dictionary for this document.

        Returns:
            dict: Basic metadata including filename, size, type and upload time.
        """
        return{
            "filename": self.original_filename,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "uploaded_at": self.uploaded_at
        }