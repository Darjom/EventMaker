from abc import ABC, abstractmethod
from typing import List, Optional
from .Event import Event


class EventRepository(ABC):
    @abstractmethod
    def save(self, event: Event) -> Event:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Event]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Event]:
        pass

    # ... otros métodos para update, delete, etc.