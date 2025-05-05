from abc import ABC, abstractmethod
from typing import List
from .DelegationTutor import DelegationTutor


class DelegationTutorRepository(ABC):
    @abstractmethod
    def save(self, delegation_tutor: DelegationTutor) -> DelegationTutor:
        pass

    @abstractmethod
    def find_by_delegation(self, delegation_id: int) -> List[DelegationTutor]:
        pass

    @abstractmethod
    def find_by_tutor(self, tutor_id: int) -> List[DelegationTutor]:
        pass

    @abstractmethod
    def get_role_name_by_tutor_and_delegation(self, tutor_id: int, delegation_id: int) -> str:
        pass