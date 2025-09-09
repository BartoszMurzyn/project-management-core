from abc import ABC, abstractmethod

from project_management_core.domain.entities.document import Document


class DocumentRepository(ABC):
    """Abstract base class defining the contract for document repository implementations.
    This repository handles persistence and retrieval of `Document` entities.
    Concrete implementations may interact with databases, APIs, or in-memory stores.
    """

    @abstractmethod
    def create(self, document: Document) -> Document:
        """Persist a new document entity.
        Args:
            document (Document): The document to be created.
        Returns:
            Document: The newly created document with any generated fields populated.
        """
        pass

    @abstractmethod
    def get_by_id(self, document_id: int) -> Document | None:
        """Retrieve a document by its unique identifier.
        Args:
            document_id (int): The ID of the document.
        Returns:
            Document | None: The matching document, or None if not found.
        """
        pass

    @abstractmethod
    def get_by_project(self, project_id: int) -> list[Document]:
        """Retrieve all documents associated with a given project.
        Args:
            project_id (int): The ID of the project.
        Returns:
            list[Document]: A list of documents linked to the project."""
        pass

    @abstractmethod
    def delete(self, document_id: int) -> None:
        """Delete a document by its unique identifier.
        Args:
            document_id (int): The ID of the document to delete.
        """
        pass
