from .dtos.EventDTO import EventDTO

from modules.events.domain.EventRepository import EventRepository


class EventQueryService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, event_id: int) -> EventDTO:
        event = self.repository.find_by_id(event_id)
        if event is None:  # Si no existe, puedes lanzar una excepción o devolver None
            return None

        return EventDTO.fromDomain(event)