# modules/areas/application/dtos/AreaDTO.py
from pydantic import BaseModel, field_validator
from typing import Optional
from modules.areas.domain.Area import Area


class AreaDTO(BaseModel):
    id_area: Optional[int] = None
    id_evento: int
    nombre_area: str
    descripcion: str
    afiche: Optional[bytes] = None
    precio: Optional[int] = None

    @field_validator('precio')
    def precio_no_negativo(cls, v):
        if v is not None and v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @classmethod
    def from_domain(cls, area: Area) -> 'AreaDTO':
        return cls(
            id_area=area.id_area,
            id_evento=area.id_evento,
            nombre_area=area.nombre_area,
            descripcion=area.descripcion,
            afiche=area.afiche,
            precio=area.precio
        )

    def to_domain(self) -> Area:
        from modules.areas.domain.Area import Area  # Import diferido
        return Area(
            id_area=self.id_area,
            id_evento=self.id_evento,
            nombre_area=self.nombre_area,
            descripcion=self.descripcion,
            afiche=self.afiche,
            precio=self.precio
        )