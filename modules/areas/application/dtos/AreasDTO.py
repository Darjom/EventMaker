from typing import List

from pydantic import BaseModel

from modules.areas.application.dtos.AreaDTO import AreaDTO


class AreasDTO(BaseModel):
    areas: List[AreaDTO]


    def getEventos(self) -> List[AreaDTO]:
        return self.areas