from project_management_core.infrastructure.config import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from project_management_core.infrastructure.repositories.db.models.db_models import Base, User
from project_management_core.infrastructure.repositories.db.db_repository import AsyncRepository
import asyncio



engine = create_async_engine(DB_URL, echo = True)
AsyncSessionLocal = sessionmaker(engine, class_= AsyncSession, expire_on_commit= False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def test_postgres_repo():
    await init_db()
    async with AsyncSessionLocal() as session:
        repo = AsyncRepository(User)

        user = await repo.create(session, {
            "email": "bartek@qwe.com",
            "password_hash": "tajne_haslo123"
        })
        print("Created: ", user.id, user.email)


asyncio.run(test_postgres_repo())
