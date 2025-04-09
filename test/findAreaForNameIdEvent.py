# test_area_finder.py
from app import app
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository

def test_find_areas_by_event_name(user_id: int = 1, name: str ="Tech sansi 2025"):

        repo = PostgresAreaRepository()
        finder = AreaFinder(repo)
        result = finder.by_name_and_event_id(name, user_id)
        if result is not None:
            print(f"\nÁrea encontrada para el evento {user_id}:")

            print(f"- {result.nombre_area} (ID: {result.id_area})")
        else:
            print("No hay coincidendias")
        #return result

if __name__ == "__main__":
    with app.app_context():
        test_find_areas_by_event_name()