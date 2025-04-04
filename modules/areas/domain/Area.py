from typing import Optional

class Area:
    def __init__(
        self,
        id_area: Optional[int],
        id_evento: int,
        nombre_area: str,
        descripcion: str,
        afiche: Optional[bytes] = None,
        precio: Optional[int] = None
    ):
        self.id_area = id_area
        self.id_evento = id_evento
        self.nombre_area = nombre_area
        self.descripcion = descripcion
        self.afiche = afiche
        self.precio = precio

        # Validaciones de negocio
        if precio is not None and precio < 0:
            raise ValueError("El precio no puede ser negativo")

        if not nombre_area:
            raise ValueError("El nombre del área es requerido")

    def __repr__(self):
        return (
            f"Area(id_area={self.id_area}, id_evento={self.id_evento}, nombre_area='{self.nombre_area}', "
            f"descripcion='{self.descripcion}', precio={self.precio}, afiche={'Yes' if self.afiche else 'No'})"
        )
