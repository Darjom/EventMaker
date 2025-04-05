from datetime import datetime

from app import app
from modules.events.application.EventCreator import EventCreator
from modules.events.application.dtos.EventDTO import EventDTO
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def test_create_event():
    # Crear un DTO de evento de prueba
    event_dto = EventDTO(
        nombre_evento="Tech sansi 2025",
        tipo_evento="Conferencia",
        descripcion_evento="Un evento sobre las últimas tendencias tecnológicas.",
        inicio_evento=datetime(2025, 5, 20, 9, 0, 0),
        fin_evento=datetime(2025, 5, 20, 18, 0, 0),
        capacidad_evento=0,
        inscripcion="Gratis",
        requisitos="Registro previo",
        ubicacion="Centro de Convenciones",
        slogan="Innovación sin límites",
        afiche=None,  # No se incluye imagen en este test
        creador_id=[1]  # Suponiendo que existe un usuario con ID 1
    )

    repository = PostgresEventsRepository()
    creator = EventCreator(repository)

    return creator.execute(event_dto)


if __name__ == "__main__":
    with app.app_context():  # Activar el contexto de la aplicación
        event_created = test_create_event()
        print("Evento creado:", event_created)



