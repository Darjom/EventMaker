from abc import ABC, abstractmethod

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