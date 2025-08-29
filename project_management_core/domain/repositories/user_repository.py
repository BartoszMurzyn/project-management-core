from abc import ABC, abstractmethod
from project_management_core.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email) -> User | None:
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id) -> None:
        pass