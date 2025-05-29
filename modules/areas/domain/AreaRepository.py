# modules/areas/domain/AreaRepository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .Area import Area


class AreaRepository(ABC):
    @abstractmethod
    def save(self, area: Area) -> Area:
        pass

    @abstractmethod
    def find_by_id(self, area_id: int) -> Optional[Area]:
        pass

    @abstractmethod
    def find_by_name_idEvent(self, name: str, event_id: int) -> Optional[Area]:
        pass

    @abstractmethod
    def find_by_event_id(self, event_id: int) -> List[Area]:
        pass

    @abstractmethod
    def update(self, area: Area) -> Area:
        pass
    