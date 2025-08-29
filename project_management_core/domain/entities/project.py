from typing import Optional
from pydantic import BaseModel, Field

# class Project:
#     def __init__(self, name: str, description: str, owner_id: int, participants: Optional[list[id]],  id: Optional[int] = None) -> None:
#         self.id = id
#         self.name = name
#         self.description = description
#         self.owner_id = owner_id
#         self.participants = participants

class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    owner_id: int
    participants: list[int] = Field(default_factory=list)

    # Adding user to a project
    def add_user(self, user_id: int) -> None:
        if not user_id:
            raise ValueError("No user found")
        elif user_id in self.participants:
            raise ValueError(f"User already in project {self.name}")
        self.participants.append(user_id)

    # Removing user from a project
    def remove_user(self, user_id: int):
        if not user_id:
            raise ValueError("No user found")
        elif user_id not in self.participants:
            raise ValueError(f"User {user_id} not found in project {self.name}")
        self.participants.remove(user_id)

    # Changing project name
    def change_name(self, new_name: str):
        if self.name == new_name:
            raise ValueError("New name can't be the same as old")
        elif not new_name:
            raise ValueError("Projects name can't be empty")
        self.name = new_name

    # Changing project description
    def change_description(self, new_description: str):
        if self.description == new_description:
            raise ValueError("New description can't be the same as old")
        elif not new_description:
            raise ValueError("Projects description can't be empty")
        self.self.description = new_description

    # Checking if user has owner rights
    def has_access(self, user_id: int) -> bool:
        if self.owner_id == user_id:
            return True
        else:
            return False


    