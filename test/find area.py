# test_area_finder.py
from app import app
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository

def test_find_areas_by_event(event_id: int = 10):

        repo = PostgresAreaRepository()
        finder = AreaFinder(repo)
        result = finder.execute(event_id)
        print(f"\nÁreas encontradas para el evento {event_id}:")
        for area in result.areas:
            print(f"- {area.nombre_area} (ID: {area.id_area})")
        return result

if __name__ == "__main__":
    with app.app_context():
        test_find_areas_by_event()