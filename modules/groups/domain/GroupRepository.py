from abc import ABC, abstractmethod
from typing import Optional, List
from .Group import Group


class GroupRepository(ABC):
    @abstractmethod
    def save(self, group: Group) -> Group:
        pass

    @abstractmethod
    def find_by_id(self, group_id: int) -> Optional[Group]:
        pass

    @abstractmethod
    def find_by_area(self, area_id: int) -> List[Group]:
        pass

    @abstractmethod
    def find_by_delegation(self, delegation_id: int) -> List[Group]:
        pass

    @abstractmethod
    def assign_tutor_to_group(self, group_id: int, tutor_id: int) -> None:
        pass

    @abstractmethod
    def get_groups_by_tutor_and_delegation(self, tutor_id: int, delegation_id: int) -> List[Group]:
        pass

    @abstractmethod
    def remove_tutor_from_group(self, group_id: int, tutor_id: int) -> bool:
        pass

    @abstractmethod
    def assign_student_to_group(self, group_id: int, student_id: int) -> None:
        pass

    @abstractmethod
    def get_students_by_group_id(self, group_id: int):
        pass

    def get_tutors_by_group_id(self, group_id: int):
        pass
