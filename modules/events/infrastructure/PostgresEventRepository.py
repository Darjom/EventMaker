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

    def find_by_name(self, name: str) -> Optional[Event]:
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