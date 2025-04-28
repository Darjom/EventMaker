from typing import Optional
from datetime import datetime

class Delegation:
    def __init__(
        self,
        id_delegacion: Optional[int] = None,
        nombre: Optional[str] = None,
        evento_id: Optional[int] = None,
        codigo: Optional[str] = None
    ):
        self.id_delegacion = id_delegacion
        self.nombre = nombre
        self.evento_id = evento_id
        self.codigo = codigo

        self._validate()

    def _validate(self):
        if not self.nombre:
            raise ValueError("El nombre de la delegación es requerido")

    def __str__(self):
        return f"Delegación({self.nombre}, Evento: {self.evento_id})"