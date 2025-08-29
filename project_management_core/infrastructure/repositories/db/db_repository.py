from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class AsyncRepository:
    def __init__(self, model):
        self.model = model
    
    async def create(self,session: AsyncSession,  obj_in: dict):
        obj = self.model(**obj_in)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
        
    async def get(self, session: AsyncSession , obj_id: int):
        result = await session.execute(select(self.model).where(self.model.id == obj_id))
        obj = result.scalar_one_or_none()
        return obj

    async def update(self, session: AsyncSession, obj_in:dict, obj_id:int ):
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
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
            )
        obj = result.scalar_one_or_none()
        await session.delete(obj)
        await session.commit()