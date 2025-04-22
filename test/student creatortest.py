from datetime import datetime
# En test/user_create.py
import sys
import os

# Añade el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from modules.students.application.StudentCreator import StudentCreator
from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository


def test_create_and_get_student():
    # Crear un DTO de estudiante de prueba
    student_dto = StudentDTO(
        first_name="Juan",
        last_name="Pérez",
        email="danielk@example.com",
        password="12345678",
        phone_number=987654321,
        ci= "12345678 b" ,
        expedito_ci= "CBBA",
        fecha_nacimiento=datetime(2025, 5, 20, 9, 0, 0),
        school_id=1,
        course="Ingeniería de Software",
        department="La Paz",
        province="Murillo"
    )

    # Configurar el servicio y repositorio
    repository = PostgresStudentRepository()
    service = StudentCreator(repository)

    # 1. Crear el estudiante
    created_student = service.create_student(student_dto)
    if created_student is not None:
        print("\nEstudiante creado exitosamente:")
        print(f"ID: {created_student.id}")
        print(f"Nombre: {created_student.first_name} {created_student.last_name}")
        print(f"Email: {created_student.email}")
        print(f"Curso: {created_student.course}")
        print("\n=== Prueba completada exitosamente ===")
        print(f"Estudiante creado con ID: {created_student.id}")
    else:
        print("No existe el colegio")

    return  created_student

if __name__ == "__main__":
    with app.app_context():  # Activar el contexto de la aplicación
        print("=== Iniciando prueba del módulo de estudiantes ===")

        created_student = test_create_and_get_student()

