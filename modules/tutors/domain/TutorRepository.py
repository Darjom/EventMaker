from abc import ABC, abstractmethod
from typing import List

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
    def assign_tutorship(self, student_id: int, tutor_id: int):
        pass

    @abstractmethod
    def update(self, tutor: Tutor) -> Tutor:
        pass

    @abstractmethod
    def find_students(self, tutor_id: int) -> List[int]:
        pass