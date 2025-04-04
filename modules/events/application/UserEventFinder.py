# application/EventFinder.py
from .dtos.EventsDTO import EventsDTO
from .dtos.EventDTO import EventDTO
from ..domain.EventRepository import EventRepository

class UserEventFinder:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, user_id: int) -> EventsDTO:
        events = self.repository.find_by_user_id(user_id)
        event_dtos = [EventDTO.fromDomain(event) for event in events]
        return EventsDTO(eventos=event_dtos)