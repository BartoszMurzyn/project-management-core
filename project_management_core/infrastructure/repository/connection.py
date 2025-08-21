from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from project_management_core.infrastructure.config import DB_URL

def get_async_engine(db_url):
    return create_async_engine(DB_URL)

def get_async_session_maker():
    engine = get_async_engine()
    return async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session():
    async_session_local = get_async_session_maker()
    async with async_session_local() as session:
        yield session