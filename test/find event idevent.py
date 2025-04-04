from app import app
from modules.events.application.EventQueryService import EventQueryService
from modules.events.application.UserEventFinder import UserEventFinder
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def test_find_events_by_user(event_id: int = 15):
    repository = PostgresEventsRepository()
    finder = EventQueryService(repository)
    return finder.execute(event_id)


if __name__ == "__main__":
    with app.app_context():

        # Prueba de búsqueda
        print("\nBuscando evento:")
        event= test_find_events_by_user()
        if event is not None:
            print(f"- {event.nombre_evento} (ID: {event.id_evento})")
        else:
            print("no existe")