from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from .Inscription import Inscription

class InscriptionRepository(ABC):
    @abstractmethod
    def save(self, inscription: Inscription) -> Inscription:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        student_id: int,
        event_id: int,
        area_id: int,
        category_id: int
    ) -> Optional[Inscription]:
        pass

    @abstractmethod
    def find_by_id_student(self, student_id: int) -> List[Inscription]:
        pass

    @abstractmethod
    def find_by_student_and_event(self, student_id: int, event_id: int) -> List[Inscription]:
        pass

    @abstractmethod
    def find_by_delegation_id(self, delegation_id: int) -> List[Inscription]:
        pass

    @abstractmethod
    def update_all(self, inscriptions: List[Inscription]) -> List[Inscription]:
        pass

    @abstractmethod
    def update(self, inscription: Inscription) -> Inscription:
        pass

    @abstractmethod
    def find_by_id(self, inscription_id: int) -> Optional[Inscription]:
        pass

    @abstractmethod
    def delete(self, inscription: Inscription) -> None:
        pass

    @abstractmethod
    def find_by_id_event(self, event_id: int) -> List[Inscription]:
        pass

    @abstractmethod
    def get_students_by_category(self,  event_id: int) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_students_by_area(self,  event_id: int) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_inscriptions_timeline(self, event_id: int) -> Dict[datetime, int]:
        pass

    @abstractmethod
    def get_completion_ratio(self, event_id: int) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_payment_status_distribution(self, event_id: int) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_inscription_funnel(self, event_id: int) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_stacked_bar_data(self,  event_id: int) -> Dict[str, Dict[str, int]]:
        pass





