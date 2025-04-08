# modules/areas/application/AreaFinder.py
from typing import List

from .dtos.EventsDTO import EventsDTO
from .dtos.EventDTO import EventDTO
from ..domain.EventRepository import EventRepository

class EventFinder:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, event_id: int) -> EventDTO:
        event = self.repository.find_by_id(event_id)
        if event is None:
            return None
        return EventDTO.fromDomain(event)

    def by_name_and_user_id(self, name: str, event_id: int) -> EventDTO:
        event = self.repository.find_by_name_userId(name, event_id)
        if event is None:  # Si no existe, puedes lanzar una excepción o devolver None
            return None
        return EventDTO.fromDomain(event)


