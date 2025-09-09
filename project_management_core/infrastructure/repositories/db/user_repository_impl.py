from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from project_management_core.domain.entities.user import User
from project_management_core.domain.repositories.user_repository import UserRepository
from project_management_core.infrastructure.repositories.db.models.db_models import (
    UserModel,
)


class RepositoryError(Exception):
    pass

class UserRecordNotFoundError(RepositoryError):
    """User not found in database."""

class UserRepositoryError(RepositoryError):
    """Problem with saving/loading user from database."""

class UserDataIntegrityError(RepositoryError):
    """Constraints validation"""

class UserRepositoryImpl(UserRepository):
    """SQLAlchemy-based implementation of the `UserRepository` interface."""
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an async database session.

        Args:
            session: Async SQLAlchemy session.
        """
        self.session = session

    
    async def create(self, user: User) -> User:
        """Persist a new user and return the stored entity.

        Args:
            user: Domain user to persist.

        Returns:
            The created `User` entity with generated fields populated.

        Raises:
            UserDataIntegrityError: On integrity constraint violations.
            UserRepositoryError: On general database errors.
        """
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
        """Fetch a user by ID.

        Args:
            user_id: Identifier of the user.

        Returns:
            The matching `User` entity.

        Raises:
            UserRecordNotFoundError: If no user exists with the given ID.
        """
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
        """Fetch a user by email.

        Args:
            email: Email address to search for.

        Returns:
            The matching `User` entity.

        Raises:
            UserRecordNotFoundError: If no user exists with the given email.
        """
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
        """List all users in the system.

        Returns:
            List of `User` entities.

        Raises:
            UserRecordNotFoundError: If the table is empty.
        """
        query = select(UserModel)
        result = await self.session.execute(query)
        orm_users = result.scalars().all()
        if not orm_users:
            raise UserRecordNotFoundError("No users found")
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
        """Update an existing user.

        Args:
            user: User with updated fields to persist.

        Returns:
            The updated `User` entity.

        Raises:
            UserRecordNotFoundError: If the user does not exist.
            UserRepositoryError: On general database errors.
        """
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
        """Delete a user by ID.

        Args:
            user_id: Identifier of the user to delete.

        Raises:
            UserRecordNotFoundError: If the user does not exist.
        """
        result = await self.session.get(UserModel, user_id)
        if result is None:
            raise UserRecordNotFoundError(f'User {user_id} could not be found.') 
        await self.session.delete(result)
        await self.session.commit()
        