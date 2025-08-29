import select
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_core.domain.repositories.project_repository import ProjectRepository
from project_management_core.domain.entities.project import Project
from typing import Optional
from project_management_core.infrastructure.repositories.db.models.db_models import ProjectModel


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, session: AsyncSession) -> None: #Czy tutaj mogę np przekazać get_async_session z connection.py?
        self.session = session

    
    async def create(self, project: Project) -> Project:
        orm_project = ProjectModel(
            id = project.id,
            name = project.name,
            description = project.description,
            owner_id = project.owner_id,
        )
        self.session.add(orm_project)
        await self.session.commit()
        await self.session.refresh(orm_project)

        return Project(
            id = orm_project.id,
            name = orm_project.name,
            description = orm_project.description,
            owner_id = orm_project.owner_id 
        )

    
    async def get_by_id(self, project_id: int) -> Optional[Project]:
        result = await self.session.get(ProjectModel, project_id)
        if result is None:
            return None
        return Project(
            id = result.id,
            name = result.name,
            description = result.description,
            owner_id = result.owner_id 
        )

    
    async def get_for_user(self, user_id: int) -> list[Project]:
        project_query = select(ProjectModel).where(ProjectModel.owner_id == user_id)
        result = await self.session.execute(project_query)
        rows = result.scalars().all()
        projects = []
        for row in rows:
            projects.append(
                Project(
            id=row.id,
            name=row.name,
            description=row.description,
            owner_id=row.owner_id
        ))
        return projects
    
    async def update(self, project: Project) -> Project:
        result = await self.session.get(ProjectModel, project.id) 
        if result is None:
            return None
        result.name = project.name
        result.description = project.description
        await self.session.commit()
        await self.session.refresh(result)

        return Project(
            id = result.id,
            name = result.name,
            description = result.description
        )

    async def delete(self, project_id: int) -> None:
        result = await self.session.get(ProjectModel, project_id)
        if result is None:
            return 
        await self.session.delete(result)
        await self.session.commit()
