from app import app
from modules.inscriptions.application.BulkInscriptionsRegistrer import BulkInscriptionsRegistrar
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository


def test_bulk_register_inscriptions():
    # Lista de IDs de estudiantes válidos en la base de datos
    students_ids = [10, 7, 8, 12, 13, 20]  # Asegúrate de que estos estudiantes existan

    # IDs válidos para evento, área, categoría y delegación
    event_id = 1
    area_id = 3
    category_id = 4
    delegation_id = 2  # Asegúrate de que sea válido para tu dominio

    # Inicializar repositorios reales
    inscription_repo = PostgresInscriptionRepository()
    student_repo = PostgresStudentRepository()
    event_repo = PostgresEventsRepository()
    area_repo = PostgresAreaRepository()
    category_repo = PostgresCategoryRepository()

    # Crear instancia del registrador masivo
    registrar = BulkInscriptionsRegistrar(
        inscription_repository=inscription_repo,
        student_repository=student_repo,
        event_repository=event_repo,
        area_repository=area_repo,
        category_repository=category_repo
    )

    # Ejecutar el registro masivo
    registrar.execute(
        students_ids=students_ids,
        event_id=event_id,
        area_id=area_id,
        category_id=category_id,
        delegation_id=delegation_id
    )

    print("✅ Inscripciones masivas realizadas correctamente.")


if __name__ == "__main__":
    with app.app_context():
        try:
            test_bulk_register_inscriptions()
        except ValueError as e:
            print(f"❌ Error durante el registro masivo: {e}")
