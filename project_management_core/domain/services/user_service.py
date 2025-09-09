import bcrypt

from project_management_core.domain.entities.user import User
from project_management_core.domain.repositories.user_repository import UserRepository


class UserError(Exception):
    """Base class for user-related errors."""
    pass

class UserNotFoundError(UserError):
    """Raised when a user cannot be found."""
    pass

class UserAlreadyDeactivatedError(UserError):
    """Raised when trying to deactivate an already inactive user."""
    pass

class UserService():
    """Application service for user registration and account management."""
    def __init__(self, user_repository: UserRepository):
        """Initialize the user service.

        Args:
            user_repository: Repository used to persist and fetch users.
        """
        self.user_repository = user_repository

    async def register_user(self, email: str, password_hash: str):
        """Register a new user with a hashed password.

        Args:
            email: Email of the user to register.
            password_hash: Raw password (will be hashed internally).

        Returns:
            The created `User` entity.
        """
        password_hashed = bcrypt.hashpw(password_hash.encode(), bcrypt.gensalt()).decode()
        user = User(
            id = None,
            email= email,
            password_hash= password_hashed,
            is_active=True
        )
        return await self.user_repository.create(user)

    async def change_user_password(self, user_id: int, new_hash: str): 
        """Change a user's password.

        Args:
            user_id: Identifier of the user.
            new_hash: New raw password to set (will be hashed).

        Returns:
            The updated `User` entity.

        Raises:
            UserNotFoundError: If the user cannot be found.
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        if user and len(new_hash) > 8:
            new_hash = bcrypt.hashpw(new_hash.encode(), bcrypt.gensalt()).decode()
            user.password_hash = new_hash
        return await self.user_repository.update(user)
    
    async def deactivate_user(self,user_id: int):
        """Deactivate a user's account.

        Args:
            user_id: Identifier of the user to deactivate.

        Returns:
            The updated `User` entity.

        Raises:
            UserNotFoundError: If the user cannot be found.
            UserAlreadyDeactivatedError: If the user is already inactive.
        """
        user =await  self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        if not user.is_active:
            raise UserAlreadyDeactivatedError("User alreadt deactivated")
        else:
            user.is_active = False
            return await self.user_repository.update(user)

    async def get_by_email(self, email: str) -> User:
        """Fetch a user by email address.

        Args:
            email: Email address to look up.

        Returns:
            The matching `User` entity.

        Raises:
            UserNotFoundError: If no user exists with that email.
        """
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    
