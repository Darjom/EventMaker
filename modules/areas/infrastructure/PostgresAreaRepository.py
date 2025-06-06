# modules/areas/infrastructure/PostgresAreaRepository.py
from typing import List, Optional
from ..domain.AreaRepository import AreaRepository
from ..domain.Area import Area
from .persistence.AreaMapping import AreaMapping
from shared.extensions import db


class PostgresAreaRepository(AreaRepository):
    def save(self, area: Area) -> Area:
        area_mapping = AreaMapping.from_domain(area)
        db.session.add(area_mapping)
        db.session.commit()
        return area_mapping.to_domain()

    def find_by_id(self, area_id: int) -> Optional[Area]:
        mapping = AreaMapping.query.get(area_id)
        return mapping.to_domain() if mapping else None

    def find_by_name_idEvent(self, name: str, event_id: int) -> Optional[Area]:
        area = AreaMapping.query.filter_by(
            nombre_area=name,
            id_evento=event_id
        ).first()
        return area.to_domain() if area else None

    def find_by_event_id(self, event_id: int) -> List[Area]:
        areas = AreaMapping.query.filter_by(id_evento=event_id).all()
        return [a.to_domain() for a in areas]

    def update(self, area: Area) -> Area:
        """Actualiza un área existente en la base de datos."""
        # Buscar el área existente
        area_mapping = AreaMapping.query.get(area.id_area)
        if not area_mapping:
            raise ValueError(f"Área con id {area.id_area} no encontrada")

        # Actualizar campos
        area_mapping.nombre_area = area.nombre_area
        area_mapping.descripcion = area.descripcion
        area_mapping.afiche = area.afiche
        area_mapping.precio = area.precio

        # El id_evento no se actualiza porque es parte de la relación
        db.session.commit()
        return area_mapping.to_domain()

