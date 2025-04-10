from datetime import datetime
from typing import Optional, List


class Event:
    def __init__(
            self,
            id_evento: Optional[int] = None,
            nombre_evento: str = "",
            tipo_evento: str = "",
            descripcion_evento: Optional[str] = None,
            inicio_evento: Optional[datetime] = None,
            fin_evento: Optional[datetime] = None,
            inicio_inscripcion: Optional[datetime] = None,
            fin_inscripcion: Optional[datetime] = None,
            capacidad_evento: Optional[int] = None,
            inscripcion: Optional[str] = None,
            requisitos: Optional[str] = None,
            ubicacion: Optional[str] = None,
            slogan: Optional[str] = None,
            afiche: Optional[str] = None,
            creador_id: Optional[List[int]] = None
    ):
        self.id_evento = id_evento
        self.nombre_evento = nombre_evento
        self.tipo_evento = tipo_evento
        self.descripcion_evento = descripcion_evento
        self.inicio_evento = inicio_evento
        self.fin_evento = fin_evento
        self.inicio_inscripcion = inicio_inscripcion
        self.fin_inscripcion = fin_inscripcion
        self.capacidad_evento = capacidad_evento
        self.inscripcion = inscripcion
        self.requisitos = requisitos
        self.ubicacion = ubicacion
        self.slogan = slogan
        self.afiche = afiche
        self.creador_id = creador_id

        # Validaciones
        if self.capacidad_evento is not None and self.capacidad_evento < 0:
            raise ValueError("La capacidad del evento no puede ser negativa.")

        if self.inicio_evento and self.fin_evento:
            if self.inicio_evento >= self.fin_evento:
                raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")
        if self.inicio_inscripcion and self.fin_inscripcion:
            if self.inicio_inscripcion >= self.fin_inscripcion:
                raise ValueError("La fecha de inicio de inscripcion debe ser anterior ala fecha fin de  inscripcion")

    def __str__(self):
        return f"Evento({self.nombre_evento}, {self.tipo_evento}, {self.inicio_evento} - {self.fin_evento})"
