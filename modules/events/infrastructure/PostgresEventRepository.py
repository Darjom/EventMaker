from typing import List, Optional
from ..domain.EventRepository import EventRepository
from ..domain.Event import Event
from .persistence.EventMapping import EventMapping
from shared.extensions import db


class PostgresEventsRepository(EventRepository):
    def save(self, event: Event) -> Event:
        event_mapping = EventMapping.from_domain(event)
        db.session.add(event_mapping)
        db.session.commit()
        return event_mapping.to_domain()

    def find_by_name(self, name: str) -> Optional[Event]:
        event_mapping = EventMapping.query.filter_by(nombre_evento=name).first()
        return event_mapping.to_domain() if event_mapping else None

    def find_by_user_id(self, user_id: int) -> List[Event]:
        event_mappings = EventMapping.query.filter_by(creador_id=user_id).all()
        return [e.to_domain() for e in event_mappings]

    # ... implementar otros métodos