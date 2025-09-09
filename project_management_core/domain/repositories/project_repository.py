from abc import ABC, abstractmethod

from project_management_core.domain.entities.project import Project


class ProjectRepository(ABC):
    """Abstract base class defining the contract for project repository implementations.
    This repository handles persistence and retrieval of `Project` entities.
    """

    @abstractmethod
    def create(self, project: Project) -> Project:
        """Persist a new project entity.
        Args:
            project (Project): The project to be created.
        Returns:
            Project: The newly created project with any generated fields populated."""
        pass      

    @abstractmethod
    def get_by_id(self, project_id: str) -> Project | None:
        """Retrieve a project by its unique identifier.
        Args:
            project_id (str): The ID of the project.
        Returns:
            Project | None: The matching project, or None if not found.
        """
        pass

    @abstractmethod
    def get_for_user(self, user_id: int) -> list[Project]:
        """Retrieve all projects associated with a given user.
        Args:
            user_id (int): The ID of the user.
        Returns:
            list[Project]: A list of projects owned by or assigned to the user.
        """
        pass

    @abstractmethod
    def update(self, project: Project) -> Project:
        """Update an existing project.
        Args:
            project (Project): The project with updated data.
        Returns:
            Project: The updated project entity.
        """
        pass 

    @abstractmethod
    def delete(self, project_id: int) -> None:
        """Delete a project by its unique identifier.
        Args:
            project_id (int): The ID of the project to delete.
        """
        pass
