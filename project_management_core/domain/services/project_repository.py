from project_management_core.domain.repositories.project_repository import ProjectRepository
from project_management_core.domain.entities.project import Project
from project_management_core.domain.services.user_service import UserNotFoundError
from project_management_core.infrastructure.repositories.db.project_repository_impl import RepositoryError

class ProjectServiceError(Exception):
    """Base class for project-related errors."""
    pass

class ProjectValidationError(ProjectServiceError):
    """Raised when project input data is invalid (e.g., empty name)."""
    pass

class ProjectNotFoundError(ProjectServiceError):
    pass

class ProjectAccessDeniedError(ProjectServiceError):
    """Raised when a user does not have rights to access or modify a project."""
    pass

class OwnerValidationError(ProjectServiceError):
    """Raised when owner_id is missing or invalid."""
    pass

class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repository = project_repo
        
    async def create_project(self, name: str, description: str, owner_id: int) -> Project:
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
        project_list = await self.project_repository.get_for_user(user_id)
        if not project_list:
            raise UserNotFoundError(f"Provided user {user_id} not found.")
        return project_list

    async def get_project(self, project_id: int) -> Project:
        try:
            return await self.project_repository.get_by_id(project_id)
        except RepositoryError as e:
            raise ProjectNotFoundError(e)

    async def update_project(self, project_id: int, name: str, description: str) -> Project:
        if not project_id:
            raise ProjectNotFoundError("Invalid project_id")
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError("Project does not exists")
        project.change_name(name)
        project.change_description(description)        
        return await self.project_repository.update(project)

    async def delete_project(self, project_id: int) -> None:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError("Project not found")
        try:    
            await self.project_repository.delete(project_id)
        except RepositoryError as e:
            raise ProjectServiceError(str(e)) 