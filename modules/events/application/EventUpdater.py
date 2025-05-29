from ..domain.EventRepository import EventRepository
from .dtos.EventDTO import EventDTO

class EventUpdater:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, event_dto: EventDTO) -> EventDTO:
        # Convertir DTO a entidad de dominio
        event = event_dto.toDomain()

        # Validar que el evento existe antes de actualizar
        existing_event = self.repository.find_by_id(event.id_evento)
        if not existing_event:
            raise ValueError("Evento no encontrado")

        # Actualizar el evento
        updated_event = self.repository.update(event)

        # Convertir de vuelta a DTO
        return EventDTO.fromDomain(updated_event)
