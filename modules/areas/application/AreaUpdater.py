from ..domain.AreaRepository import AreaRepository
from .dtos.AreaDTO import AreaDTO

class AreaUpdater:
    def __init__(self, repository: AreaRepository):
        self.repository = repository

    def execute(self, area_dto: AreaDTO) -> AreaDTO:
        # Convertir DTO a entidad de dominio
        area = area_dto.to_domain()

        # Validar que el área existe antes de actualizar
        existing_area = self.repository.find_by_id(area.id_area)
        if not existing_area:
            raise ValueError("Área no encontrada")

        # Actualizar el área
        updated_area = self.repository.update(area)

        # Convertir de vuelta a DTO
        return AreaDTO.from_domain(updated_area)
