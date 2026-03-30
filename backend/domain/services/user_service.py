import re
from domain.entities.user import User
from domain.ports.user_repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user: User) -> User:
        if not user.username:
            user.username = self.suggest_username(user.first_name, user.last_name)
        return self.repo.save(user)

    def suggest_username(self, first_name: str, last_name: str) -> str:
        base = f"{first_name}.{last_name}".lower()
        base = re.sub(r"[^a-z0-9.]", "", base)
        username = base
        counter = 1
        while self.repo.username_exists(username):
            username = f"{base}{counter}"
            counter += 1
        return username

    def list_users(self, skip: int, limit: int) -> tuple[list[User], int]:
        return self.repo.list(skip, limit)

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)