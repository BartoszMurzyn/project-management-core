from abc import ABC, abstractmethod
from project_management_core.domain.entities.project import Project


class ProjectRepository(ABC):

    @abstractmethod
    def create(self, project: Project) -> Project:
        pass      

    @abstractmethod
    def get_by_id(self, project_id: str) -> Project | None:
        pass

    @abstractmethod
    def get_for_user(self, user_id: int) -> list[Project]:
        pass

    @abstractmethod
    def update(self, project: Project) -> Project:
        pass 

    @abstractmethod
    def delete(self, project_id: int) -> None:
        pass
