# application/ActiveEventFinder.py
from .dtos.EventsDTO import EventsDTO
from .dtos.EventDTO import EventDTO
from ..domain.EventRepository import EventRepository


class ActiveEventFinder:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self) -> EventsDTO:
        active_events = self.repository.find_active_events()
        event_dtos = [EventDTO.fromDomain(event) for event in active_events]
        return EventsDTO(eventos=event_dtos)