from app import app
from modules.events.application.UserEventFinder import UserEventFinder
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def test_find_events_by_user(user_id: int = 100):
    repository = PostgresEventsRepository()
    finder = UserEventFinder(repository)
    return finder.execute(user_id)


if __name__ == "__main__":
    with app.app_context():

        # Prueba de búsqueda
        print("\nBuscando eventos del usuario 1:")
        found_events = test_find_events_by_user()
        for event in found_events.eventos:
            print(f"- {event.nombre_evento} (ID: {event.id_evento})")