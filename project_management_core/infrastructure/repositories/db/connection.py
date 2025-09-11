from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from project_management_core.infrastructure.config import DB_URL
from project_management_core.infrastructure.repositories.db.models.db_models import Base

engine = create_async_engine(DB_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def init_models():
    """Create tables if they don’t exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session():
    async with async_session_maker() as session:
        yield session