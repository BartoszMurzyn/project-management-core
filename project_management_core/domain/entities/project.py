from pydantic import BaseModel, Field


class UserError(Exception):
    pass

class UserNotFoundError(UserError):
    """User not found."""
    pass

class UserAlreadyInProjectError(UserError):
    """User is already a participant."""
    pass

class UserNotInProjectError(UserError):
    """User is not a participant."""
    pass

class UserNotOwnerError(UserError):
    """User is not an owner of the project."""
    pass

class UserUnauthorizedError(UserError):
    """User has not authorization."""
    pass 

class ProjectError(Exception):
    """Base class for all project-related errors."""
    pass

class EmptyProjectError(ProjectError):
    """Project name can't be empty."""
    pass

class EmptyDescriptionError(ProjectError):
    """Project description can't be empty."""
    pass

class Project(BaseModel):
    """Domain entity representing a project and its participants."""
    id: int | None = None
    name: str
    description: str
    owner_id: int
    participants: list[int] = Field(default_factory=list)

    def add_user(self, user_id: int) -> None:
        """Add a user to the project's participants.

        Args:
            user_id: Identifier of the user to add.

        Raises:
            UserNotFoundError: If `user_id` is falsy.
            UserAlreadyInProjectError: If the user is already a participant.
        """
        if not user_id:
            raise UserNotFoundError("No user found")
        elif user_id in self.participants:
            raise UserAlreadyInProjectError(f"User already in project {self.name}")
        self.participants.append(user_id)

    def remove_user(self, user_id: int):
        """Remove a user from the project's participants.

        Args:
            user_id: Identifier of the user to remove.

        Raises:
            ValueError: If `user_id` is falsy.
            UserNotInProjectError: If the user is not a participant.
        """
        if not user_id:
            raise ValueError("No user found")
        elif user_id not in self.participants:
            raise UserNotInProjectError(f"User {user_id} not found in project {self.name}")
        self.participants.remove(user_id)

    
    def change_name(self, new_name: str):
        """Change the project's name.

        Args:
            new_name: New name for the project.

        Raises:
            ValueError: If the new name is the same as the current name.
            EmptyProjectError: If the new name is empty.
        """
        if self.name == new_name:
            raise ValueError("New name can't be the same as old")
        elif not new_name:
            raise EmptyProjectError("Projects name can't be empty")
        self.name = new_name

    
    def change_description(self, new_description: str):
        """Change the project's description.

        Args:
            new_description: New description for the project.

        Raises:
            ValueError: If the new description is the same as the current description.
            EmptyDescriptionError: If the new description is empty.
        """
        if self.description == new_description:
            raise ValueError("New description can't be the same as old")
        elif not new_description:
            raise EmptyDescriptionError("Projects description can't be empty")
        self.description = new_description

    
    def has_access(self, user_id: int) -> bool:
        """Check whether a user has access rights to the project.

        Args:
            user_id: Identifier of the user to check.

        Returns:
            True if the user is the owner or a participant.

        Raises:
            UserUnauthorizedError: If the user is neither owner nor participant.
        """
        if self.owner_id != user_id and user_id not in self.participants:
            raise UserUnauthorizedError("User has no rights to access this project")
        return True


    