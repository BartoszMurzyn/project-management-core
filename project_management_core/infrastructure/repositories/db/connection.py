from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from project_management_core.infrastructure.config import DB_URL
from project_management_core.infrastructure.repositories.db.models.db_models import Base

async def init_models(engine):
    """Create tables if they don’t exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_async_engine():
    engine = create_async_engine(DB_URL)
    # Fire and forget: create tables on startup
    import asyncio
    asyncio.get_event_loop().create_task(init_models(engine))
    return engine

def get_async_session_maker():
    engine = get_async_engine()
    return async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session():
    async_session_local = get_async_session_maker()
    async with async_session_local() as session:
        yield session