from modules.events.domain.EventRepository import EventRepository


class EventDeleter:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, event_id: int):
        self.repository.delete(event_id)
        

