from abc import ABC, abstractmethod
from typing import List

from modules.permissions.domain.Permission import Permission
from modules.tutors.domain.Tutor import Tutor


class TutorRepository(ABC):
    @abstractmethod
    def save(self, tutor: Tutor) -> None:
        pass

    @abstractmethod
    def add_roles_to_user(self, tutor_id: int, role_ids: List[int]) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Tutor:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Tutor:
        pass

    @abstractmethod
    def find_by_ci(self, ci: int) -> Tutor:
        pass

    @abstractmethod
    def get_delegation_permissions(self, tutor_id: int, delegation_id: int) -> List[Permission]:
        pass