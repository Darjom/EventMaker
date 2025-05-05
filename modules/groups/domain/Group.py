from typing import Optional


class Group:
    def __init__(
            self,
            id_grupo: Optional[int] = None,
            nombre_grupo: Optional[str] = None,
            id_area: Optional[int] = None,
            id_delegacion: Optional[int] = None
    ):
        self.id_grupo = id_grupo
        self.nombre_grupo = nombre_grupo
        self.id_area = id_area
        self.id_delegacion = id_delegacion

        self._validate()

    def _validate(self):
        if not self.nombre_grupo:
            raise ValueError("El nombre del grupo es requerido")
        if not self.id_area:
            raise ValueError("El área es requerida")
        if not self.id_delegacion:
            raise ValueError("La delegación es requerida")

    def __str__(self):
        return f"Grupo({self.nombre_grupo}, Área: {self.id_area}, Delegación: {self.id_delegacion})"