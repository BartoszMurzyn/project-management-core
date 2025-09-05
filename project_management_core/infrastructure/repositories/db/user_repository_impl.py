from sqlalchemy import select
from project_management_core.domain.entities.user import User
from project_management_core.domain.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_core.infrastructure.repositories.db.models.db_models import UserModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class RepositoryError(Exception):
    pass

class UserRecordNotFoundError(RepositoryError):
    """User not found in database."""

class UserRepositoryError(RepositoryError):
    """Problem with saving/loading user from database."""

class UserDataIntegrityError(RepositoryError):
    """Constraints validation"""

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    
    async def create(self, user: User) -> User:
        orm_user = UserModel(
            id = user.id,
            email = user.email,
            password_hash = user.password_hash,
        )
        try:
            self.session.add(orm_user)
            await self.session.commit()
            await self.session.refresh(orm_user)
        except IntegrityError as e:
            raise UserDataIntegrityError(f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise UserRepositoryError(f"Database error: {e}")

        return User(
            id = orm_user.id,
            email= orm_user.email,
            password_hash= orm_user.password_hash,
            is_active= True
        )

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.get(UserModel, user_id)
        if result is None:
            raise UserRecordNotFoundError(f"No user found with ID: {user_id}")
        return User(
            id = result.id,
            email= result.email,
            password_hash= result.password_hash,
            is_active= True
        )

    async def get_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        orm_user = result.scalar_one_or_none()
        if orm_user is None:
            raise UserRecordNotFoundError(f"No user found with email: {email}")
        return User(
            id = orm_user.id,
            email= orm_user.email,
            password_hash= orm_user.password_hash,
            is_active= True
        )

    async def list_all(self) -> list[User] :
        query = select(UserModel)
        result = await self.session.execute(query)
        orm_users = result.scalars().all()
        if not orm_users:
            raise UserRecordNotFoundError(f"No users found")
        users = []
        for orm_user in orm_users:
            user = User(
                id=orm_user.id,
                email=orm_user.email,
                password_hash=orm_user.password_hash,
                is_active=True
            )
            users.append(user)
        return users


    async def update(self, user: User) -> User | None:
        result = await self.session.get(UserModel, user.id)
        if result is None:
            raise UserRecordNotFoundError(f"Could not find user: {user}")
        try:
            result.email = user.email
            result.password_hash = user.password_hash
            await self.session.commit()
            await self.session.refresh(result)
        except SQLAlchemyError as e:
            raise UserRepositoryError(f"Could not update user {user.id}: {e}")

        return User(
            id = result.id,
            email= result.email,
            password_hash= result.password_hash,
            is_active= True
        )

    async def delete(self, user_id: int) -> None:
        result = await self.session.get(UserModel, user_id)
        if result is None:
            raise UserRecordNotFoundError(f'User {user_id} could not be found.') 
        await self.session.delete(result)
        await self.session.commit()
        