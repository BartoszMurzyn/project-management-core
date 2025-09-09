from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from project_management_core.domain.entities.document import Document
from project_management_core.domain.repositories.document_repository import (
    DocumentRepository,
)
from project_management_core.infrastructure.repositories.db.models.db_models import (
    DocumentModel,
)


class RepositoryError(Exception):
    pass

class DocumentRecordNotFoundError(RepositoryError):
    """Document not found in database."""

class DocumentRepositoryError(RepositoryError):
    """Problem with saving/loading document"""

class DocumentDataIntegrityError(RepositoryError):
    """Constraints validation"""


class DocumentRepositoryImpl(DocumentRepository):
    """SQLAlchemy-based implementation of the `DocumentRepository` interface."""
    def __init__(self, session: AsyncSession):
        """Initialize the repository with an async database session.

        Args:
            session: Async SQLAlchemy session.
        """
        self.session = session
    
    async def create(self, document: Document) -> Document:
        """Persist a new document and return the stored entity.

        Args:
            document: Domain document to persist.

        Returns:
            The created `Document` entity with generated fields populated.

        Raises:
            DocumentDataIntegrityError: On integrity constraint violations.
            DocumentRepositoryError: On general database errors.
        """
        orm_document = DocumentModel(
            id = document.id,
            original_filename = document.original_filename,
            generated_filename = document.generated_filename,
            file_path = document.file_path,
            file_size = document.file_size,
            content_type = document.content_type,
            project_id = document.project_id,
            uploaded_by = document.uploaded_by,
            uploaded_at = document.uploaded_at
        )
        try:
            self.session.add(orm_document)
            await self.session.commit()
            await self.session.refresh(orm_document)
        except IntegrityError as e:
            raise DocumentDataIntegrityError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise DocumentRepositoryError(f"Database error: {e}")

        return Document(
            id = orm_document.id,
            original_filename = orm_document.original_filename,
            generated_filename = orm_document.generated_filename,
            file_path = orm_document.file_path,
            file_size = orm_document.file_size,
            content_type = orm_document.content_type,
            project_id = orm_document.project_id,
            uploaded_by = orm_document.uploaded_by,
            uploaded_at = orm_document.uploaded_at
        )
    
    async def get_by_id(self, document_id: int) -> Document | None:
        """Fetch a document by ID.

        Args:
            document_id: Identifier of the document.

        Returns:
            The matching `Document` entity.

        Raises:
            DocumentRecordNotFoundError: If the document does not exist.
        """
        result = await self.session.get(DocumentModel, document_id)
        if result is None:
            raise DocumentRecordNotFoundError(f"No document found with ID: {document_id}")
        return Document(
            id = result.id,
            original_filename = result.original_filename,
            generated_filename = result.generated_filename,
            file_path = result.file_path,
            file_size = result.file_size,
            content_type = result.content_type,
            project_id = result.project_id,
            uploaded_by = result.uploaded_by,
            uploaded_at = result.uploaded_at
        )

    async def get_by_project(self, project_id: int) -> list[Document]:
        """Fetch all documents for the given project ID.

        Args:
            project_id: Project identifier.

        Returns:
            List of `Document` entities.

        Raises:
            DocumentRecordNotFoundError: If no documents are found for the project.
        """
        query = select(DocumentModel).where(DocumentModel.project_id == project_id)
        result = await self.session.execute(query)
        orm_documents = result.scalars().all()
        if not orm_documents:
            raise DocumentRecordNotFoundError(f"No documents founds for project {project_id}")
        return  [Document(
            id = doc.id,
            original_filename = doc.original_filename,
            generated_filename = doc.generated_filename,
            file_path = doc.file_path,
            file_size = doc.file_size,
            content_type = doc.content_type,
            project_id = doc.project_id,
            uploaded_by = doc.uploaded_by,
            uploaded_at = doc.uploaded_at
        )
        for doc in orm_documents
        ]
    
    async def delete(self, document_id: int) -> None:
        """Delete a document by ID.

        Args:
            document_id: Identifier of the document to delete.

        Raises:
            DocumentRecordNotFoundError: If the document does not exist.
        """
        result = await self.session.get(DocumentModel, document_id)
        if result is None:
            raise DocumentRecordNotFoundError(f'Document {document_id} could not be found.') 
        await self.session.delete(result)
        await self.session.commit()
