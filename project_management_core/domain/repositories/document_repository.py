from abc import ABC, abstractmethod
from project_management_core.domain.entities.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def create(self, document: Document) -> Document:
        pass

    @abstractmethod
    def get_by_id(self, document_id: int) -> Document | None:
        pass

    @abstractmethod
    def get_by_project(self, project_id: int) -> list[Document]:
        pass

    @abstractmethod
    def delete(self, document_id: int) -> None:
        pass
