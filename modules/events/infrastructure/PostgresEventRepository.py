from datetime import datetime
from typing import List, Optional
from ..domain.EventRepository import EventRepository
from ..domain.Event import Event
from .persistence.EventMapping import EventMapping
from shared.extensions import db
from ...user.infrastructure.persistence.UserMapping import UserMapping


class PostgresEventsRepository(EventRepository):
    def save(self, event: Event) -> Event:
        # Guardamos el evento en la base de datos
        event_mapping = EventMapping.from_domain(event)
        db.session.add(event_mapping)
        db.session.commit()  # Esto guarda el evento y genera un id_evento

        # Ahora que el evento tiene un id_evento, añadimos las relaciones en la tabla intermedia
        for user_id in event.creador_id:
            user = UserMapping.query.get(user_id)  # Obtienes el usuario por su id
            if user:  # Si el usuario existe en la base de datos
                event_mapping.users.append(user)  # Agregar el usuario a la relación
        db.session.commit()  # Hacemos commit para guardar la relación en la tabla intermedia

        return event_mapping.to_domain()

    def find_by_name_userId(self, name: str, user_id : int) -> Optional[Event]:
        event_mapping = EventMapping.query.filter_by(nombre_evento=name).first()
        return event_mapping.to_domain() if event_mapping else None

    def find_by_id(self, event_id: int) -> Optional[Event]:
        event_mapping = EventMapping.query.get(event_id)  # 🔍 Busca por ID
        return event_mapping.to_domain() if event_mapping else None

    def find_by_user_id(self, user_id: int) -> List[Event]:
        # consulta para usar la relación many-to-many
        event_mappings = EventMapping.query.filter(
            EventMapping.users.any(UserMapping.id == user_id)
        ).all()
        return [e.to_domain() for e in event_mappings]

    def find_active_events(self) -> List[Event]:
        now = datetime.utcnow()  # Usar UTC para consistencia
        event_mappings = EventMapping.query.filter(
            EventMapping.fin_evento >= now
        ).all()
        return [e.to_domain() for e in event_mappings]

    def update(self, event: Event) -> Event:
        """Actualiza un evento existente en la base de datos."""
        # Buscar el evento existente
        event_mapping = EventMapping.query.get(event.id_evento)
        if not event_mapping:
            raise ValueError(f"Evento con id {event.id_evento} no encontrado")

        # Actualizar campos básicos
        event_mapping.nombre_evento = event.nombre_evento
        event_mapping.tipo_evento = event.tipo_evento
        event_mapping.descripcion_evento = event.descripcion_evento
        event_mapping.inicio_evento = event.inicio_evento
        event_mapping.fin_evento = event.fin_evento
        event_mapping.inicio_inscripcion = event.inicio_inscripcion
        event_mapping.fin_inscripcion = event.fin_inscripcion
        event_mapping.capacidad_evento = event.capacidad_evento
        event_mapping.inscripcion = event.inscripcion
        event_mapping.requisitos = event.requisitos
        event_mapping.ubicacion = event.ubicacion
        event_mapping.slogan = event.slogan
        event_mapping.afiche = event.afiche

        # Actualizar relación con usuarios (creadores)
        # Limpiar relaciones existentes
        event_mapping.users = []

        # Añadir nuevos creadores
        for user_id in event.creador_id:
            user = UserMapping.query.get(user_id)
            if user:
                event_mapping.users.append(user)
            else:
                raise ValueError(f"Usuario con id {user_id} no encontrado")

        db.session.commit()
        return event_mapping.to_domain()

    def delete(self, event_id: int):
        """Elimina un evento y deja que la eliminación en cascada se encargue de las relaciones."""
        event_mapping = EventMapping.query.get(event_id)

        if not event_mapping:
            raise ValueError(f"Evento con id {event_id} no encontrado")

        db.session.delete(event_mapping)
        db.session.commit()

    