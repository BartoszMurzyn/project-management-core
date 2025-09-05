from pydantic import BaseModel
from datetime import datetime

class Document(BaseModel):
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
        return{
            "filename": self.original_filename,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "uploaded_at": self.uploaded_at
        }