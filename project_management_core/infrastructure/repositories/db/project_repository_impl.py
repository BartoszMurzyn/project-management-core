from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_core.domain.repositories.project_repository import ProjectRepository
from project_management_core.domain.entities.project import Project
from typing import Optional
from project_management_core.infrastructure.repositories.db.models.db_models import ProjectModel, ProjectMember

class RepositoryError(Exception):
    pass

class ProjectNotFoundError(RepositoryError):
      """Project not found in database."""

class ProjectRepositoryError(RepositoryError):
    """Problem with saving/loading user from database."""

class ProjectDataIntegrityError(RepositoryError):
    """Constraints validation"""


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
        try:
            self.session.add(orm_project)
            await self.session.commit()
            await self.session.refresh(orm_project)
        except SQLAlchemyError:
            await self.session.rollback()
            raise RepositoryError("Unable to create project.")
        except IntegrityError as e:
            raise ProjectDataIntegrityError(f"Integrity error: {e}")

        return Project(
            id = orm_project.id,
            name = orm_project.name,
            description = orm_project.description,
            owner_id = orm_project.owner_id,
            participants=[m.user_id for m in orm_project.members]
        )

    
    async def get_by_id(self, project_id: int) -> Optional[Project]:
        result = await self.session.get(ProjectModel, project_id)
        if result is None:
            
            raise ProjectNotFoundError("Project not found")
        

        return Project(
            id = result.id,
            name = result.name,
            description = result.description,
            owner_id = result.owner_id ,
            participants = [m.user_id for m in result.members]
        )

    
    async def get_for_user(self, user_id: int) -> list[Project]:
        project_query = select(ProjectModel).where(ProjectModel.owner_id == user_id)
        result = await self.session.execute(project_query)
        rows = result.scalars().all()
        if not rows:
            raise ProjectNotFoundError(f"No projects found for user: {user_id}")
        projects = []
        for row in rows:
            projects.append(
                Project(
            id=row.id,
            name=row.name,
            description=row.description,
            owner_id=row.owner_id,
            participants = [m.user_id for m in result.members]
        ))
        return projects
    
    async def update(self, project: Project) -> Project:
        result = await self.session.get(ProjectModel, project.id) 
        if result is None:
            raise ProjectNotFoundError("Project not found")
        try:
            result.name = project.name
            result.description = project.description
            
            await self.session.commit()
            await self.session.refresh(result)
        except SQLAlchemyError as e:
            raise ProjectRepositoryError(f"Could not update project {project.id}: {e}")

        return Project(
            id = result.id,
            name = result.name,
            description = result.description,
            owner_id= result.owner_id,
            participants = [m.user_id for m in result.members]
        )
    
    async def add_user_to_project(self, project_id: int, user_id: int) -> Project:
        """Add a single user to a project as a participant."""
        project_result = await self.session.get(ProjectModel, project_id, options=[selectinload(ProjectModel.members)])
        if not project_result:
            raise ProjectNotFoundError("Project not found")
        
        # Check if user is already a participant
        for member in project_result.members:
            if member.user_id == user_id:
                raise ProjectDataIntegrityError(f"User {user_id} is already a participant in project {project_id}")

        if user_id == project_result.owner_id:
            raise ProjectDataIntegrityError("Project owner cannot be added as participant")

        try:
            member = ProjectMember(user_id=user_id, project_id=project_id, role="participant")
            self.session.add(member)
            await self.session.commit()
            await self.session.refresh(project_result)  # Refresh to include new member
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ProjectRepositoryError(f"Could not add user to project: {e}")

        return Project(
            id=project_result.id,
            name=project_result.name,
            description=project_result.description,
            owner_id=project_result.owner_id,
            participants=[m.user_id for m in project_result.members]  # Now includes newly added member
        )

    async def delete(self, project_id: int) -> None:
        try:
            result = await self.session.get(ProjectModel, project_id)
            await self.session.delete(result)
            await self.session.commit()
        except SQLAlchemyError:
            raise RepositoryError("Unable to delete project.")