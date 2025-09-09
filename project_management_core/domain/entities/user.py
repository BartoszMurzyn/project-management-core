class UserEntityError(Exception):
    """Base class for all User entity errors."""
    pass

class UserPasswordSameAsOldError(UserEntityError):
    """Raised when the new password is the same as the old one."""
    pass

class UserPasswordEmptyError(UserEntityError):
    """Raised when the new password is empty."""
    pass

class UserAlreadyDeactivatedError(UserEntityError):
    """Raised when trying to deactivate an already inactive user."""
    pass

class UserAlreadyActivatedError(UserEntityError):
    """Raised when trying to activate an already active user."""
    pass

class User:
    """Domain entity representing a user of the system.

    Holds identity and authentication state, and exposes operations
    related to account lifecycle such as password change and activation.
    """
    def __init__(self, id: int, email: str, password_hash: str, is_active: bool = True):
        """Initialize a new `User` entity.

        Args:
            id: Unique identifier of the user.
            email: Email address of the user.
            password_hash: Hashed password.
            is_active: Whether the account is active. Defaults to True.
        """
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active

    def change_password(self, new_hash: str):
        """Set a new password hash for the user.

        Args:
            new_hash: New password hash to set.

        Raises:
            UserPasswordSameAsOldError: If the new hash equals the old hash.
            UserPasswordEmptyError: If the new hash is empty.
        """
        if new_hash == self.password_hash:
            raise UserPasswordSameAsOldError("New password can't be the same as old one")
        elif not new_hash:
            raise UserPasswordEmptyError("New password can't be empty")
        self.password_hash = new_hash
        
    def deactivate(self):
        """Deactivate the user account.

        Raises:
            UserAlreadyDeactivatedError: If the account is already inactive.
        """
        if not self.is_active:
            raise UserAlreadyDeactivatedError("User is already deactivated")
        self.is_active = False

    def activate(self):
        """Activate the user account.

        Raises:
            UserAlreadyActivatedError: If the account is already active.
        """
        if self.is_active:
            raise UserAlreadyActivatedError("User is already activated")
        self.is_active = True