from abc import ABC, abstractmethod
from typing import Optional, List
from .Delegation import Delegation

class DelegationRepository(ABC):
    @abstractmethod
    def save(self, delegation: Delegation) -> Delegation:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Delegation]:
        pass

    @abstractmethod
    def find_by_event_id(self, event_id: int) -> list[Delegation]:
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Delegation]:
        pass

    @abstractmethod
    def find_by_ids(self, delegation_ids: List[int]) -> List[Delegation]:
        pass


    @abstractmethod
    def assign_student_to_delegation(self, delegation_id: int, student_id: int) -> bool:
        pass

    @abstractmethod
    def get_student_ids_by_delegation_id(self, delegation_id: int) -> list[int]:
        pass


    @abstractmethod
    def find_by_delegation_id(self, delgation_id: int) -> Optional[Delegation]:
        pass

    @abstractmethod
    def get_tutor_ids_by_delegation_id(self, delegation_id: int) -> list[int]:
        pass