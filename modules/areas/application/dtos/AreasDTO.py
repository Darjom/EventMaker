from typing import List

from pydantic import BaseModel

from modules.areas.application.dtos.AreaDTO import AreaDTO


class AreasDTO(BaseModel):
    areas: List[AreaDTO]


    @classmethod
    def from_domain_list(cls, areas: list):
        return cls(
            areas=[AreaDTO.from_domain(area) for area in areas]
        )