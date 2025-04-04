from datetime import datetime, timedelta
from app import app
from modules.events.application.ActiveEventFinder import ActiveEventFinder
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def test_find_active_events():
    repository = PostgresEventsRepository()
    finder = ActiveEventFinder(repository)
    return finder.execute()


if __name__ == "__main__":
    with app.app_context():
        # Prueba de eventos vigentes
        print("\nEventos vigentes:")
        active_events = test_find_active_events()

        for event in active_events.eventos:
            status = "VIGENTE" if event.fin_evento > datetime.utcnow() else "FINALIZADO"
            print(f"- {event.nombre_evento} | Fin: {event.fin_evento} | Estado: {status}")