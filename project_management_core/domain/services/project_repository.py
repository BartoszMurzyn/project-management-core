from project_management_core.domain.repositories.project_repository import ProjectRepository
from project_management_core.domain.entities.project import Project

class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repository = project_repo
        
    async def create_project(self, name: str, description: str, owner_id: int) -> Project:
        if not name or not name.strip():
            raise ValueError("Project name is required")
        if not description or not description.strip():
            raise ValueError("Project description is required")
        elif owner_id is None or owner_id <= 0:
            raise ValueError("Owner ID must be a positive integer")
        project = Project(
            id = None,
            name = name.strip(),
            description= description.strip(),
            owner_id= owner_id
        )
        return await self.project_repository.create(project)

    async def get_projects_for_user(self, user_id: int) -> list[Project]:
        if not user_id:
            raise ValueError("Invalid user_id")
        project_list = await self.project_repository.get_for_user(user_id)
        return project_list

    async def update_project(self, project_id: int, name: str, description: str) -> Project:
        if not project_id:
            raise ValueError("Invalid project_id")
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("Project does not exists")
        project.change_name(name)
        project.change_description(description)        
        return await self.project_repository.update(project)

    async def delete_project(self, project_id: int, user_id: int) -> None:
        # projects = await self.project_repository.get_for_user(user_id)
        # if projects is None:
        #     raise ValueError(f"User {user_id} does not have access to delete project")
        # for project in projects:
        #     if project.id == project_id:
        #         await self.project_repository.delete(project_id)
            
        # raise ValueError("User has no access to this project")
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise ValueError("Project not found")
        if project.has_access(user_id):
            await self.project_repository.delete(project_id)
        else:
            raise ValueError(f"User {user_id} has no rights to delete project")