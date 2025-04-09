# test_area_finder.py
from app import app
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.application.EventFinder import EventFinder
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def test_find_event_by_event_name(event_id: int = 8, name: str ="prueba"):

        repo = PostgresEventsRepository()
        finder = EventFinder(repo)
        result = finder.by_name_and_user_id(name, event_id)
        if result is not None:
            print(f"\nEvento encontrado para el usuario {event_id}:")

            print(f"- {result.nombre_evento} (ID: {result.id_evento})")
        else:
            print("No hay coincidendias")
        #return result

if __name__ == "__main__":
    with app.app_context():
        test_find_event_by_event_name()