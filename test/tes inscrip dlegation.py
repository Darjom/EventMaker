import json
from app import app
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.application.GetStudentInscriptionsByDelegation import GetStudentInscriptionsByDelegation
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository


def test_get_student_inscriptions_by_delegation(delegation_id: int = 1):
    # Instanciar repositorios concretos
    inscription_repo = PostgresInscriptionRepository()
    student_repo = PostgresStudentRepository()
    event_repo = PostgresEventsRepository()
    area_repo = PostgresAreaRepository()
    category_repo = PostgresCategoryRepository()

    # Crear caso de uso PASANDO PARÁMETROS POSICIONALES
    usecase = GetStudentInscriptionsByDelegation(
        inscription_repo,
        student_repo,
        event_repo,
        area_repo,
        category_repo
    )

    return usecase.execute(delegation_id)

if __name__ == "__main__":
    with app.app_context():
        delegation_id = 1  # O cualquier ID de delegación que quieras probar
        print(f"\nBuscando inscripciones para la delegación {delegation_id}:")
        grouped = test_get_student_inscriptions_by_delegation(delegation_id)
        if grouped is None:
            print("No exite la inscripciones")

        # Imprime la estructura del diccionario como JSON bonito
        print("\n📦 Estructura completa del diccionario:\n")
        print(json.dumps(grouped, indent=4, ensure_ascii=False))

        if not grouped:
            print("No se encontraron inscripciones para la delegación.")
        else:
            for student_name, student_info in grouped.items():
                print(f"\nEstudiante: {student_name} (Curso: {student_info['curso']})")
                for ins in student_info['inscripciones']:
                    print(
                        f"  - Área: {ins['area_name']}, "
                        f"Categoría: {ins['category_name']}, "
                        f"Monto: {ins['category_monto']}"
                    )
