# modules/areas/application/AreaFinder.py
from typing import List, Optional

from .dtos.AreasDTO import AreasDTO
from .dtos.AreaDTO import AreaDTO
from ..domain.AreaRepository import AreaRepository

class AreaFinder:
    def __init__(self, repository: AreaRepository):
        self.repository = repository

    #Trae todas las areas de un evento o convocatoria
    def execute(self, event_id: int) -> AreasDTO:
        areas = self.repository.find_by_event_id(event_id)
        area_dtos = [AreaDTO.from_domain(area) for area in areas]
        return AreasDTO(areas=area_dtos)


    #Trae todas las areas que tiene el mismo nombre y estas asociadas al mismo evento.
    #garantiza que no se creen areas con el mismo nombre para el mismo evento
    def by_name_and_event_id(self, name: str, event_id: int) -> AreaDTO:

        area = self.repository.find_by_name_idEvent(name, event_id)
        if area is None:  # Si no existe, puedes lanzar una excepción o devolver None
            return None
        return AreaDTO.from_domain(area)

    def find_by_id(self, area_id: int) -> Optional[AreaDTO]:
        area = self.repository.find_by_id(area_id)
        if area is None:
            return None
        return AreaDTO.from_domain(area)
