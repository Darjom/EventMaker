from abc import ABC, abstractmethod
from typing import Optional
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