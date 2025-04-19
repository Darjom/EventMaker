from .dtos.EventsDTO import EventsDTO
from .dtos.EventDTO import EventDTO
from ..domain.EventRepository import EventRepository
import random

class RandomActiveEventFinder:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self) -> EventsDTO:
        active_events = self.repository.find_active_events()
        random.shuffle(active_events)  # Mezclar aleatoriamente
        selected = active_events[:6]  # Tomar solo 6
        return EventsDTO(eventos=[EventDTO.fromDomain(e) for e in selected])
