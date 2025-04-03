from .dtos.EventDTO import EventDTO
from ..domain.EventRepository import EventRepository



class EventCreator:

    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, event_dto: EventDTO) -> EventDTO:
        event = event_dto.toDomain()
        saved_event = self.repository.save(event)
        return EventDTO.fromDomain(saved_event)
