import json
from app import app
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.inscriptions.GetInscriptionsByEvent import GetInscriptionsByEvent
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.application.GetStudentById import GetStudentById
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository



def test_get_inscriptions_by_event(event_id: int = 1):
    # Instanciar repositorios concretos
    inscription_repo = PostgresInscriptionRepository()
    student_service = GetStudentById(PostgresStudentRepository())
    area_service = PostgresAreaRepository()
    category_service = PostgresCategoryRepository()

    # Crear caso de uso
    usecase = GetInscriptionsByEvent(
        inscription_repo,
        student_service,
        area_service,
        category_service
    )

    # Ejecutar y devolver el resultado
    return usecase.execute(event_id)


if __name__ == "__main__":
    with app.app_context():
        event_id = 1  # O el ID de evento que quieras probar
        print(f"\nBuscando inscripciones para el evento {event_id}:\n")
        grouped = test_get_inscriptions_by_event(event_id)
        if not grouped:
            print("No se encontraron inscripciones para el evento.")
        else:
            # Imprime estructura completa como JSON bonito
            print(json.dumps(grouped, indent=4, ensure_ascii=False))

            # Ejemplo de recorrido simplificado
            for area_name, area_info in grouped.items():
                print(f"\nÁrea: {area_name} (ID: {area_info['id']})")
                for cat_name, cat_info in area_info['categories'].items():
                    print(f"  Categoría: {cat_name} (ID: {cat_info['id']})")
                    for ins in cat_info['inscriptions']:
                        print(
                            f"    - Estudiante: {ins['student_name']} "
                            f"(ID: {ins['student_id']}), Curso: {ins.get('course')}, "
                            f"Estado: {ins['status']}, Fecha: {ins['inscription_date']}"
                        )
