from abc import ABC, abstractmethod

from project_management_core.domain.entities.user import User


class UserRepository(ABC):
    """Abstract base class defining the contract for user repository implementations.
    This repository handles persistence and retrieval of `User` entities.
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """Persist a new user entity.
        Args:
            user (User): The user to be created.
        Returns:
            User: The newly created user with any generated fields populated.
        """
        pass

    @abstractmethod
    def get_by_id(self, user_id) -> User | None:
        """Retrieve a user by their unique identifier.
        Args:
            user_id: The ID of the user.
        Returns:
            User | None: The matching user, or None if not found.
        """
        pass

    @abstractmethod
    def get_by_email(self, email) -> User | None:
        """Retrieve a user by their email address.
        Args:
            email (str): The email address of the user.
        Returns:
            User | None: The matching user, or None if not found.
        """
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        """Retrieve all users.
        Returns:
            list[User]: A list of all user entities.
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user.
        Args:
            user (User): The user with updated data.
        Returns:
            User: The updated user entity.
        """
        pass

    @abstractmethod
    def delete(self, user_id) -> None:
        """Delete a user by their unique identifier.
        Args:
            user_id: The ID of the user to delete.
        """
        pass