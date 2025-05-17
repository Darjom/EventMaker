# En test/user_create.py
import sys
import os

# Añade el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from app import app
from modules.tutors.application.TutorCreator import TutorCreator
from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository


def test_create_and_get_tutor():

    tutor_dto = TutorDTO(
        first_name="Juan",
        last_name="Pérez",
        email="jjquiquegfk@example.com",
        password="12345678",
        ci= "12345678 BA",
        expedito_ci= "CBBA",
        fecha_nacimiento=datetime(2025, 5, 20, 9, 0, 0),
    )

    # Configurar el servicio y repositorio
    repository = PostgresTutorRepository()
    service = TutorCreator(repository)

    # 1. Crear el estudiante
    created_tutor = service.create_tutor(tutor_dto)
    if created_tutor is not None:
        print("\ntutor creado exitosamente:")
        print(f"ID: {created_tutor.id}")
        print(f"Nombre: {created_tutor.first_name} {created_tutor.last_name}")
        print(f"Email: {created_tutor.email}")
        print (f"expedito: {created_tutor.expedito_ci}")

    else:
        print("No existe el colegio")

    return created_tutor

if __name__ == "__main__":
    with app.app_context():  # Activar el contexto de la aplicación
        print("=== Iniciando prueba del módulo de estudiantes ===")

        created_student = test_create_and_get_tutor()

