from pydantic import BaseModel, Field
NotFoundError = type("NotFoundError", (Exception, ), {})
EmptyProjectError = type("EmptyProjectError", (Exception, ), {})
EmptyDescriptionError = type("EmptyDescriptionError", (Exception, ), {})


class Project(BaseModel):
    id: int | None = None
    name: str
    description: str
    owner_id: int
    participants: list[int] = Field(default_factory=list)

    def add_user(self, user_id: int) -> None:
        """Adds a user to a project"""
        if not user_id:
            raise NotFoundError("No user found")
        elif user_id in self.participants:
            raise ValueError(f"User already in project {self.name}")
        self.participants.append(user_id)

    def remove_user(self, user_id: int):
        """Removing user from a project"""
        if not user_id:
            raise ValueError("No user found")
        elif user_id not in self.participants:
            raise ValueError(f"User {user_id} not found in project {self.name}")
        self.participants.remove(user_id)

    
    def change_name(self, new_name: str):
        """Changing project name"""
        if self.name == new_name:
            raise ValueError("New name can't be the same as old")
        elif not new_name:
            raise EmptyProjectError("Projects name can't be empty")
        self.name = new_name

    
    def change_description(self, new_description: str):
        """Changing project description"""
        if self.description == new_description:
            raise ValueError("New description can't be the same as old")
        elif not new_description:
            raise EmptyDescriptionError("Projects description can't be empty")
        self.description = new_description

    
    def has_access(self, user_id: int) -> bool:
        """Checking if user has owner rights"""
        if self.owner_id == user_id:
            return True
        else:
            return False


    