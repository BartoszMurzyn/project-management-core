from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from project_management_core.domain.entities.project import Project
from project_management_core.domain.repositories.project_repository import (
    ProjectRepository,
)
from project_management_core.infrastructure.repositories.db.models.db_models import (
    ProjectModel,
)


class RepositoryError(Exception):
    pass

class ProjectNotFoundError(RepositoryError):
      """Project not found in database."""

class ProjectRepositoryError(RepositoryError):
    """Problem with saving/loading user from database."""

class ProjectDataIntegrityError(RepositoryError):
    """Constraints validation"""


class ProjectRepositoryImpl(ProjectRepository):
    """SQLAlchemy-based implementation of the `ProjectRepository` interface."""
    def __init__(self, session: AsyncSession) -> None: #Czy tutaj mogę np przekazać get_async_session z connection.py?
        """Initialize the repository with an async database session.

        Args:
            session: Async SQLAlchemy session.
        """
        self.session = session

    
    async def create(self, project: Project) -> Project:
        """Persist a new project and return the stored entity.

        Args:
            project: Domain project to persist.

        Returns:
            The created `Project` entity with generated fields populated.

        Raises:
            RepositoryError: On general database errors.
            ProjectDataIntegrityError: On integrity constraint violations.
        """
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
            owner_id = orm_project.owner_id 
        )

    
    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Fetch a project by ID.

        Args:
            project_id: Identifier of the project.

        Returns:
            The matching `Project` entity.

        Raises:
            ProjectNotFoundError: If the project does not exist.
        """
        result = await self.session.get(ProjectModel, project_id)
        if result is None:
            raise ProjectNotFoundError("Project not found")

        return Project(
            id = result.id,
            name = result.name,
            description = result.description,
            owner_id = result.owner_id 
        )

    
    async def get_for_user(self, user_id: int) -> list[Project]:
        """Fetch all projects for a given owner user ID.

        Args:
            user_id: Owner user identifier.

        Returns:
            List of `Project` entities.

        Raises:
            ProjectNotFoundError: If no projects are found for the user.
        """
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
            owner_id=row.owner_id
        ))
        return projects
    
    async def update(self, project: Project) -> Project:
        """Update an existing project.

        Args:
            project: Project with updated fields to persist.

        Returns:
            The updated `Project` entity.

        Raises:
            ProjectNotFoundError: If the project does not exist.
            ProjectRepositoryError: On general database errors.
        """
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
            owner_id= result.owner_id
        )

    async def delete(self, project_id: int) -> None:
        """Delete a project by ID.

        Args:
            project_id: Identifier of the project to delete.

        Raises:
            RepositoryError: If the delete operation fails.
        """
        try:
            result = await self.session.get(ProjectModel, project_id)
            await self.session.delete(result)
            await self.session.commit()
        except SQLAlchemyError:
            raise RepositoryError("Unable to delete project.")
