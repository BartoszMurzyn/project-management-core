import os
from typing import BinaryIO
from uuid import uuid4

from project_management_core.domain.entities.document import Document
from project_management_core.domain.repositories.document_repository import (
    DocumentRepository,
)


class DocumentError(Exception):
    """Base class for all document-related errors."""
    pass

class DocumentNotFoundError(DocumentError):
    """Document not found."""
    pass

class DocumentPermissionError(DocumentError):
    """User has no permission to perform this action on the document."""
    pass

class DocumentFilenameRequiredError(DocumentError):
    """Filename is required for upload."""
    pass




class DocumentService:
    """Application service for managing document uploads and lifecycle."""
    def __init__(self, document_repository: DocumentRepository, upload_dir: str = "uploads"):
        """Initialize the document service.

        Args:
            document_repository: Repository used to persist documents.
            upload_dir: Directory where uploaded files are stored. Defaults to "uploads".
        """
        self.document_repository = document_repository
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def upload_document(
        self,
        file: BinaryIO,
        original_filename: str,
        content_type: str,
        project_id: int,
        uploaded_by: int
    ) -> Document:
        """Upload a file and persist its `Document` record.

        Args:
            file: File-like object open for reading binary data.
            original_filename: Original name of the uploaded file.
            content_type: MIME type of the uploaded file.
            project_id: Identifier of the project the document belongs to.
            uploaded_by: Identifier of the uploading user.

        Returns:
            The created `Document` entity.

        Raises:
            DocumentFilenameRequiredError: If the original filename is empty.
        """
        if not original_filename:
            raise DocumentFilenameRequiredError("Filename is required")

        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        with open(file_path, "wb") as f:
            f.write(file.read())

        file_size = os.path.getsize(file_path)

        document = Document(
            original_filename=original_filename,
            generated_filename=unique_filename,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
            project_id=project_id,
            uploaded_by=uploaded_by
        )
        return await self.document_repository.create(document)
    
    async def get_documents_for_project(self, project_id: int) -> list[Document]:
        """Return all documents for a given project.

        Args:
            project_id: Identifier of the project.

        Returns:
            A list of `Document` entities.
        """
        return await self.document_repository.get_by_project(project_id)

    async def delete_document(self, document_id: int, user_id: int) -> None:
        """Delete a document if the user has permission and remove the file.

        Args:
            document_id: Identifier of the document to delete.
            user_id: Identifier of the user requesting deletion.

        Raises:
            DocumentNotFoundError: If the document does not exist.
            DocumentPermissionError: If the user did not upload the document.
        """
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError("Document not found")
        
        if document.uploaded_by != user_id:
            raise DocumentPermissionError("No permission to delete this document")
        
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        await self.document_repository.delete(document_id)