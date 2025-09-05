from project_management_core.domain.repositories.document_repository import DocumentRepository
from project_management_core.domain.entities.document import Document
import os
from uuid import uuid4
from typing import BinaryIO

class DocumentService:
    def __init__(self, document_repository: DocumentRepository, upload_dir: str = "uploads"):
        self.document_repository = document_repository
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok= True)


    async def upload_document(self, file: BinaryIO, original_filename: str,
     content_type: str, project_id: int, uploaded_by: int) -> Document:
        if original_filename is None:
            raise ValueError("Filename is required")
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        with open(file_path, "wb") as f:
            f.write(file.read())

        file_size = os.path.getsize(file_path)

        document = Document(
            original_filename= original_filename,
            generated_filename= unique_filename,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
            project_id=project_id,
            uploaded_by=uploaded_by
        )
        return await self.document_repository.create(document)
    
    async def get_documents_for_project(self, project_id:int):
            return await self.document_repository.get_by_project(project_id)

    async def delete_document(self, document_id: int, user_id: int) -> None:
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            raise ValueError("Document not found")
        
        if document.uploaded_by != user_id:
            raise ValueError("No permission to delete this document")
        
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        await self.document_repository.delete(document_id)        