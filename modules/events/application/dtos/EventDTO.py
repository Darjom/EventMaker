from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from modules.events.domain.Event import Event # Importa la entidad de dominio

class EventDTO(BaseModel):
    id_evento: Optional[int]
    nombre_evento: str
    tipo_evento: str
    descripcion_evento: Optional[str]
    inicio_evento: Optional[datetime]
    fin_evento: Optional[datetime]
    capacidad_evento: Optional[int]
    inscripcion: Optional[str]
    requisitos: Optional[str]
    ubicacion: Optional[str]
    slogan: Optional[str]
    afiche: Optional[bytes]
    creador_id: Optional[int]

    @classmethod
    def fromDomain(cls, event: Event) -> "EventDTO":
        """
        Convierte un objeto de dominio Event a un DTO EventDTO.
        """
        return cls(
            id_evento=event.id_evento,
            nombre_evento=event.nombre_evento,
            tipo_evento=event.tipo_evento,
            descripcion_evento=event.descripcion_evento,
            inicio_evento=event.inicio_evento,
            fin_evento=event.fin_evento,
            capacidad_evento=event.capacidad_evento,
            inscripcion=event.inscripcion,
            requisitos=event.requisitos,
            ubicacion=event.ubicacion,
            slogan=event.slogan,
            afiche=event.afiche,
            creador_id=event.creador_id,
        )

    def toDomain(self) -> Event:
        """
        Convierte el DTO EventDTO en un objeto de dominio Event.
        """
        return Event(
            id_evento=self.id_evento,
            nombre_evento=self.nombre_evento,
            tipo_evento=self.tipo_evento,
            descripcion_evento=self.descripcion_evento,
            inicio_evento=self.inicio_evento,
            fin_evento=self.fin_evento,
            capacidad_evento=self.capacidad_evento,
            inscripcion=self.inscripcion,
            requisitos=self.requisitos,
            ubicacion=self.ubicacion,
            slogan=self.slogan,
            afiche=self.afiche,
            creador_id=self.creador_id,
        )
