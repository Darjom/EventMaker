from abc import ABC, abstractmethod
from typing import List

from modules.user.domain.User import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def add_roles_to_user(self, user_id: int, role_ids: List[int]) -> None:
        pass

    