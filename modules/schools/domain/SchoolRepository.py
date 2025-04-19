# modules/schools/domain/SchoolRepository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .School import School

class SchoolRepository(ABC):
    @abstractmethod
    def save(self, school: School) -> School:
        pass

    @abstractmethod
    def find_by_id(self, school_id: int) -> Optional[School]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[School]:
        pass

    @abstractmethod
    def find_all(self) -> List[School]:
        pass