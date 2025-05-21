from abc import ABC, abstractmethod
from typing import List

from modules.students.domain.Student import Student


class StudentRepository(ABC):
    @abstractmethod
    def save(self, student: Student) -> None:
        pass

    @staticmethod
    def add_roles_to_user(self, user_id: int, role_ids: List[int]) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Student:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Student:
        pass

    @abstractmethod
    def find_by_ci(self, ci: str) -> Student:
        pass

    @abstractmethod
    def find_students_by_list_id(self, list_id: List[int]) -> list[Student]:
        pass
