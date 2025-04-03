# modules/areas/application/AreaFinder.py
from .dtos.AreasDTO import AreasDTO
from .dtos.AreaDTO import AreaDTO
from ..domain.AreaRepository import AreaRepository

class AreaFinder:
    def __init__(self, repository: AreaRepository):
        self.repository = repository

    def execute(self, event_id: int) -> AreasDTO:
        areas = self.repository.find_by_event_id(event_id)
        area_dtos = [AreaDTO.from_domain(area) for area in areas]
        return AreasDTO(areas=area_dtos)