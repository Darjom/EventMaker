from app import app
from modules.areas.application.AreaCreator import AreaCreator
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def test_create_area():
    # Crear un DTO de área de prueba
    area_dto = AreaDTO(
        id_evento=1,  # Debes asegurarte que exista un evento con este ID
        nombre_area="Area 5",
        descripcion="Área exclusiva con servicios fremiun",
        precio=None,
        afiche=None
    )

    # Inicializar repositorios
    area_repository = PostgresAreaRepository()
    event_repository = PostgresEventsRepository()  # Para validar existencia del evento

    # Inicializar creador de áreas
    creator = AreaCreator(area_repository, event_repository)

    return creator.execute(area_dto)


if __name__ == "__main__":
    with app.app_context():  # Activar el contexto de la aplicación

        # Ahora crear el área
        area_created = test_create_area()
        print(f"Área creada: ID={area_created.id_area}, Datos={area_created}")
