from project_management_core.domain.entities.project import Project
from project_management_core.domain.entities.user import User

from project_management_core.domain.repositories.project_repository import (
    ProjectRepository,
)
from project_management_core.domain.services.user_service import UserNotFoundError
from project_management_core.infrastructure.repositories.db.project_repository_impl import (
    RepositoryError,
)


class ProjectServiceError(Exception):
    """Base class for project-related errors."""
    pass

class ProjectValidationError(ProjectServiceError):
    """Raised when project input data is invalid (e.g., empty name)."""
    pass

class ProjectNotFoundError(ProjectServiceError):
    """Raised when a requested project cannot be found."""
    pass

class ProjectAccessDeniedError(ProjectServiceError):
    """Raised when a user does not have rights to access or modify a project."""
    pass

class OwnerValidationError(ProjectServiceError):
    """Raised when owner_id is missing or invalid."""
    pass

class ProjectService:
    """Application service for managing `Project` entities.

    Coordinates validation and repository interactions for creating,
    retrieving, updating, and deleting projects.
    """
    def __init__(self, project_repo: ProjectRepository):
        """Initialize the service with a project repository implementation.

        Args:
            project_repo: Concrete implementation of `ProjectRepository`.
        """
        self.project_repository = project_repo
        
    async def create_project(self, name: str, description: str, owner_id: int) -> Project:
        """Create a new project.

        Args:
            name: Project name; leading/trailing whitespace will be trimmed.
            description: Project description; leading/trailing whitespace will be trimmed.
            owner_id: Identifier of the user who owns the project.

        Returns:
            The newly created `Project`.

        Raises:
            ProjectServiceError: If the repository operation fails.
        """
        try:
            project = Project(
                id = None,
                name = name.strip(),
                description= description.strip(),
                owner_id= owner_id
            )
            return await self.project_repository.create(project)
        except RepositoryError as e:
            raise ProjectServiceError(str(e))
            
    async def get_projects_for_user(self, user_id: int) -> list[Project]:
        """Retrieve all projects owned by a user.

        Args:
            user_id: Identifier of the user.

        Returns:
            A list of `Project` instances.

        Raises:
            ProjectNotFoundError: If the user has no projects.
        """
        project_list = await self.project_repository.get_for_user(user_id)
        if not project_list:
            raise ProjectNotFoundError(f"Projects not found for user {user_id}.")
        return project_list

    async def get_project(self, project_id: int) -> Project:
        """Retrieve a project by its identifier.

        Args:
            project_id: Identifier of the project.

        Returns:
            The matching `Project`.

        Raises:
            ProjectNotFoundError: If the project cannot be retrieved.
        """
        try:
            return await self.project_repository.get_by_id(project_id)
        except RepositoryError as e:
            raise ProjectNotFoundError(e)

    async def update_project(self, project_id: int, name: str, description: str) -> Project:
        """Update a project's name and description.

        Args:
            project_id: Identifier of the project to update.
            name: New project name.
            description: New project description.

        Returns:
            The updated `Project`.

        Raises:
            ProjectNotFoundError: If `project_id` is invalid or the project does not exist.
        """
        if not project_id:
            raise ProjectNotFoundError("Invalid project_id")
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError("Project does not exists")
        project.change_name(name)
        project.change_description(description)        
        return await self.project_repository.update(project)

    async def delete_project(self, project_id: int) -> None:
        """Delete a project by its identifier.

        Args:
            project_id: Identifier of the project to delete.

        Raises:
            ProjectNotFoundError: If the project does not exist.
            ProjectServiceError: If the repository delete operation fails.
        """
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError("Project not found")
        try:    
            await self.project_repository.delete(project_id)
        except RepositoryError as e:
            raise ProjectServiceError(str(e)) 
    
    async def add_user_to_project(self, project_id: int, user_id: int, current_user: User) -> Project:
        project = await self.get_project(project_id)
        if not project.has_access(current_user.id):  # Changed from current_user_id.id to current_user.id
            raise ProjectAccessDeniedError("Only project owner can invite participants")
        return await self.project_repository.add_user_to_project(project_id, user_id)