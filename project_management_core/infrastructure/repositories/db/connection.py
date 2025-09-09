# db.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from project_management_core.infrastructure.config import DB_URL
from project_management_core.infrastructure.repositories.db.models.db_models import Base

# 1. Create a single global engine
engine = create_async_engine(DB_URL, echo=True)

# 2. Create a single global sessionmaker
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# 3. Function to create all tables (for dev / testing)
async def init_models():
    """Create tables if they don’t exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 4. Dependency for FastAPI routes (provides session per request)
async def get_async_session():
    async with async_session_maker() as session:
        yield session