from abc import ABC, abstractmethod
from typing import List, Optional
from .Event import Event


class EventRepository(ABC):
    @abstractmethod
    def save(self, event: Event) -> Event:
        pass

    @abstractmethod
    def find_by_id(self, event_id: int) -> Optional[Event]:
        pass
    @abstractmethod
    def find_by_name_userId(self, name: str, user_id: int) -> Optional[Event]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Event]:
        pass

    @abstractmethod
    def find_active_events(self) -> List[Event]:
        pass

    @abstractmethod
    def update(self, event: Event) -> Event:
        pass

    @abstractmethod
    def delete(self, event_id: int):
        pass
