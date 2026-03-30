from abc import ABC, abstractmethod
from domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def list(self, skip: int, limit: int) -> tuple[list[User], int]:
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        pass