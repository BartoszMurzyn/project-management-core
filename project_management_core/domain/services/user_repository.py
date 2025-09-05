from project_management_core.domain.repositories.user_repository import UserRepository
from project_management_core.domain.entities.user import User
import bcrypt

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
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, email: str, password_hash: str):
        password_hashed = bcrypt.hashpw(password_hash.encode(), bcrypt.gensalt()).decode()
        user = User(
            id = None,
            email= email,
            password_hash= password_hashed,
            is_active=True
        )
        return await self.user_repository.create(user)

    async def change_user_password(self, user_id: int, new_hash: str): 
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        if user and len(new_hash) > 8:
            new_hash = bcrypt.hashpw(new_hash.encode(), bcrypt.gensalt()).decode()
            user.password_hash = new_hash
        return await self.user_repository.update(user)
    
    async def deactivate_user(self,user_id: int):
        user =await  self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        if not user.is_active:
            raise UserAlreadyDeactivatedError("User alreadt deactivated")
        else:
            user.is_active = False
            return await self.user_repository.update(user)

    async def get_by_email(self, email: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundError("User not found")
        return user