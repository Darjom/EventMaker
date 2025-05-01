from pydantic import BaseModel
from typing import Optional

from modules.groups.domain.Group import Group


class GroupDTO(BaseModel):
    id_grupo: Optional[int] = None
    nombre_grupo: Optional[str] = None
    id_area: Optional[int] = None
    id_delegacion: Optional[int] = None

    @classmethod
    def from_domain(cls, group: Group):
        return cls(
            id_grupo=group.id_grupo,
            nombre_grupo=group.nombre_grupo,
            id_area=group.id_area,
            id_delegacion=group.id_delegacion
        )

    def to_domain(self):

        return Group(
            id_grupo=self.id_grupo,
            nombre_grupo=self.nombre_grupo,
            id_area=self.id_area,
            id_delegacion=self.id_delegacion
        )