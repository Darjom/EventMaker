# modules/areas/application/AreaCreator.py
from ..domain.AreaRepository import AreaRepository
from .dtos.AreaDTO import AreaDTO
from modules.events.domain.EventRepository import EventRepository


class AreaCreator:
    def __init__(
            self,
            area_repository: AreaRepository,
            event_repository: EventRepository  # Para validar que el evento existe
    ):
        self.area_repo = area_repository
        self.event_repo = event_repository

    def execute(self, area_dto: AreaDTO) -> AreaDTO:
        # Validar que el evento existe
        event = self.event_repo.find_by_id(area_dto.id_evento)
        if not event:
            raise ValueError("El evento asociado no existe")

        # Convertir DTO a entidad y validar reglas de negocio
        area = area_dto.to_domain()

        # Verificar nombre único por evento
        existing_area = self.area_repo.find_by_name(
            area.nombre_area,
            area.id_evento
        )
        if existing_area:
            raise ValueError("Ya existe un área con ese nombre para este evento")

        # Guardar
        saved_area = self.area_repo.save(area)

        return AreaDTO.from_domain(saved_area)