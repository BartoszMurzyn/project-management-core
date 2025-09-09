from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AsyncRepository:
    """Generic async repository helper for basic CRUD operations using SQLAlchemy."""
    def __init__(self, model, session: AsyncSession):
        """Initialize the helper with a model and session.

        Args:
            model: SQLAlchemy declarative model class.
            session: Async SQLAlchemy session instance.
        """
        self.model = model
        self.session = session
    
    async def create(self,session,  obj_in: dict):
        """Create a new record for the model.

        Args:
            session: Async session to use.
            obj_in: Mapping of fields for the new object.

        Returns:
            The created ORM model instance.
        """
        obj = self.model(**obj_in)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
        
    async def get(self, session: AsyncSession , obj_id: int):
        """Retrieve an object by ID.

        Args:
            session: Async session to use.
            obj_id: Identifier of the object.

        Returns:
            ORM instance if found, otherwise None.
        """
        result = await session.execute(select(self.model).where(self.model.id == obj_id))
        obj = result.scalar_one_or_none()
        return obj

    async def update(self, session: AsyncSession, obj_in:dict, obj_id:int ):
        """Update fields on an existing object.

        Args:
            session: Async session to use.
            obj_in: Mapping of fields to update.
            obj_id: Identifier of the object to update.

        Returns:
            The updated ORM model instance, or None if not found.
        """
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
            )
        obj = result.scalar_one_or_none()

        if not obj:
            return None
        
        for key, value in obj_in.items():
            setattr(obj, key, value)
        
        await session.commit()
        await session.refresh(obj)

        return obj

    async def delete(self, session: AsyncSession, obj_id:int):
        """Delete an object by ID.

        Args:
            session: Async session to use.
            obj_id: Identifier of the object to delete.
        """
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
            )
        obj = result.scalar_one_or_none()
        await session.delete(obj)
        await session.commit()