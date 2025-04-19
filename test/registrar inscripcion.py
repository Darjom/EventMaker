from datetime import date, time

from app import app
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.application.InscriptionRegister import InscriptionRegistrar

from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO

from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository





def test_register_inscription():
    # Crear un DTO de inscripción de prueba
    inscription_dto = InscriptionDTO(
        student_id=6,     # Asegúrate de que existan estos IDs
        event_id=1,
        area_id=1,
        category_id=3  # o time(hour=10, minute=30)
    )

    # Inicializar repositorios
    inscription_repo = PostgresInscriptionRepository()
    student_repo = PostgresStudentRepository()
    event_repo = PostgresEventsRepository()
    area_repo = PostgresAreaRepository()
    category_repo = PostgresCategoryRepository()

    # Crear instancia del registrador
    registrar = InscriptionRegistrar(
        inscription_repository=inscription_repo,
        student_repository=student_repo,
        event_repository=event_repo,
        area_repository=area_repo,
        category_repository=category_repo
    )

    # Ejecutar el registro
    return registrar.execute(inscription_dto)

if __name__ == "__main__":
    with app.app_context():
        try:
            result = test_register_inscription()
            print(f"Inscripción creada correctamente: {result}")
        except ValueError as e:
            print(f"Error durante el registro: {e}")
