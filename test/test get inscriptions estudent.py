import json

from app import app
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.application.GetAllStudentInscriptions import GetAllStudentInscriptions
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository


from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository



def test_get_student_inscriptions(student_id: int = 6):
    # Instanciar repositorios concretos
    inscription_repo = PostgresInscriptionRepository()
    student_repo = PostgresEstudentRepository()
    event_repo = PostgresEventsRepository()
    area_repo = PostgresAreaRepository()
    category_repo = PostgresCategoryRepository()

    # Crear caso de uso
    usecase = GetAllStudentInscriptions(
        inscription_repository=inscription_repo,
        student_repository=student_repo,
        event_repository=event_repo,
        area_repository=area_repo,
        category_repository=category_repo
    )
    return usecase.execute(student_id)


if __name__ == "__main__":
    with app.app_context():
        student_id = 12
        print(f"\nBuscando inscripciones del estudiante {student_id}:")
        grouped = test_get_student_inscriptions(student_id)

        # 👇 Aquí imprimes la estructura del diccionario como JSON bonito
        print("\n📦 Estructura completa del diccionario:\n")
        print(json.dumps(grouped, indent=4, ensure_ascii=False))

        if not grouped:
            print("No se encontraron inscripciones para el estudiante.")
        else:
            for event in grouped:
                print(f"\nEvento: {event['event_name']} (ID: {event['event_id']})")
                for ins in event['inscriptions']:
                    print(
                        f"  - Área: {ins['area_name']} (ID: {ins['area_id']}), "
                        f"Categoría: {ins['category_name']} (ID: {ins['category_id']}), "
                        f"Fecha: {ins['inscription_date']}, Estado: {ins['status']}"
                    )
