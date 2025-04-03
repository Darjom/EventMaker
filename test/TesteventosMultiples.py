from datetime import datetime
from app import app
from modules.events.application.EventCreator import EventCreator
from modules.events.application.dtos.EventDTO import EventDTO
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository


def create_test_events():
    # Crear los objetos EventDTO
    event1 = EventDTO(
        nombre_evento="Tech Conference 2025",
        tipo_evento="Conferencia",
        descripcion_evento="Un evento sobre las últimas tendencias tecnológicas.",
        inicio_evento=datetime(2025, 5, 20, 9, 0, 0),
        fin_evento=datetime(2025, 5, 20, 18, 0, 0),
        capacidad_evento=500,
        inscripcion="Gratis",
        requisitos="Registro previo",
        ubicacion="Centro de Convenciones",
        slogan="Innovación sin límites",
        afiche=None,
        creador_id=[1]
    )

    event2 = EventDTO(
        nombre_evento="Desarrollo Web 2025",
        tipo_evento="Taller",
        descripcion_evento="Un taller práctico sobre desarrollo web con las últimas tecnologías.",
        inicio_evento=datetime(2025, 6, 5, 10, 0, 0),
        fin_evento=datetime(2025, 6, 5, 17, 0, 0),
        capacidad_evento=100,
        inscripcion="Pago",
        requisitos="Conocimientos básicos de HTML y CSS",
        ubicacion="Sala A",
        slogan="Aprende haciendo",
        afiche=None,
        creador_id=[2]
    )

    event3 = EventDTO(
        nombre_evento="Hackathon AI",
        tipo_evento="Competencia",
        descripcion_evento="Una competencia de programación en inteligencia artificial.",
        inicio_evento=datetime(2025, 7, 10, 9, 0, 0),
        fin_evento=datetime(2025, 7, 10, 23, 59, 59),
        capacidad_evento=200,
        inscripcion="Gratis",
        requisitos="Conocimientos en Python y machine learning",
        ubicacion="Auditorio Principal",
        slogan="Codifica el futuro",
        afiche=None,
        creador_id=[3]
    )

    event4 = EventDTO(
        nombre_evento="Ciberseguridad 2025",
        tipo_evento="Seminario",
        descripcion_evento="Un seminario sobre las últimas amenazas en ciberseguridad y cómo protegerte.",
        inicio_evento=datetime(2025, 8, 15, 9, 0, 0),
        fin_evento=datetime(2025, 8, 15, 17, 0, 0),
        capacidad_evento=300,
        inscripcion="Gratis",
        requisitos="Conocimientos básicos de redes",
        ubicacion="Sala B",
        slogan="Protege tu información",
        afiche=None,
        creador_id=[1]
    )

    event5 = EventDTO(
        nombre_evento="Digital Marketing Summit",
        tipo_evento="Conferencia",
        descripcion_evento="Una conferencia sobre las últimas tendencias en marketing digital.",
        inicio_evento=datetime(2025, 9, 1, 9, 0, 0),
        fin_evento=datetime(2025, 9, 1, 18, 0, 0),
        capacidad_evento=500,
        inscripcion="Pago",
        requisitos="Experiencia en marketing digital",
        ubicacion="Auditorio C",
        slogan="Transforma tu marca",
        afiche=None,
        creador_id=[2]
    )

    event6 = EventDTO(
        nombre_evento="Desafío de Innovación",
        tipo_evento="Competencia",
        descripcion_evento="Una competencia para encontrar soluciones innovadoras a problemas sociales.",
        inicio_evento=datetime(2025, 10, 5, 8, 0, 0),
        fin_evento=datetime(2025, 10, 5, 18, 0, 0),
        capacidad_evento=100,
        inscripcion="Gratis",
        requisitos="Ideas innovadoras y creatividad",
        ubicacion="Centro de Innovación",
        slogan="Cambia el mundo",
        afiche=None,
        creador_id=[3]
    )

    event7 = EventDTO(
        nombre_evento="IoT Summit 2025",
        tipo_evento="Conferencia",
        descripcion_evento="Una conferencia sobre las últimas tendencias en Internet de las Cosas.",
        inicio_evento=datetime(2025, 11, 15, 9, 0, 0),
        fin_evento=datetime(2025, 11, 15, 18, 0, 0),
        capacidad_evento=400,
        inscripcion="Pago",
        requisitos="Conocimientos básicos de tecnología",
        ubicacion="Auditorio D",
        slogan="Conectando el futuro",
        afiche=None,
        creador_id=[1]
    )

    event8 = EventDTO(
        nombre_evento="Game Dev Conference 2025",
        tipo_evento="Conferencia",
        descripcion_evento="Conferencia sobre el desarrollo de videojuegos, desde la programación hasta el diseño.",
        inicio_evento=datetime(2025, 12, 10, 9, 0, 0),
        fin_evento=datetime(2025, 12, 10, 18, 0, 0),
        capacidad_evento=250,
        inscripcion="Gratis",
        requisitos="Interés en videojuegos",
        ubicacion="Centro de Convenciones",
        slogan="Crea tu propio juego",
        afiche=None,
        creador_id=[2]
    )

    event9 = EventDTO(
        nombre_evento="Blockchain for Beginners",
        tipo_evento="Curso",
        descripcion_evento="Un curso introductorio sobre blockchain y criptomonedas.",
        inicio_evento=datetime(2025, 6, 10, 10, 0, 0),
        fin_evento=datetime(2025, 6, 10, 17, 0, 0),
        capacidad_evento=150,
        inscripcion="Gratis",
        requisitos="Ninguno, solo ganas de aprender",
        ubicacion="Auditorio E",
        slogan="Descubre la tecnología del futuro",
        afiche=None,
        creador_id=[3]
    )

    event10 = EventDTO(
        nombre_evento="Artificial Intelligence Workshop",
        tipo_evento="Taller",
        descripcion_evento="Taller sobre inteligencia artificial aplicada a negocios.",
        inicio_evento=datetime(2025, 5, 25, 9, 0, 0),
        fin_evento=datetime(2025, 5, 25, 17, 0, 0),
        capacidad_evento=120,
        inscripcion="Pago",
        requisitos="Conocimientos en programación",
        ubicacion="Sala F",
        slogan="Transforma tu negocio con AI",
        afiche=None,
        creador_id=[1]
    )

    # Colocar los eventos en una lista
    events = [event1, event2, event3, event4, event5, event6, event7, event8, event9, event10]

    # Crear los eventos en la base de datos
    repository = PostgresEventsRepository()
    creator = EventCreator(repository)

    for event in events:
        creator.execute(event)
        print(f"Evento creado: {event.nombre_evento}")


if __name__ == "__main__":
    with app.app_context():
        create_test_events()
