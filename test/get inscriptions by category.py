# --------------------------------------------------------
# Script de prueba para GetStudentInscriptionsByCategory
# --------------------------------------------------------
import json
from app import app
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.students.application.GetStudentById import GetStudentById
from modules.schools.application.FindSchoolById import FindSchoolById

from modules.inscriptions.application.GetStudentInscriptionsByCategory import GetStudentInscriptionsByCategory


def test_get_students_by_event_by_category(event_id: int = 1):
    # Instanciar repositorios y servicios
    inscription_repo = PostgresInscriptionRepository()
    student_service = GetStudentById(PostgresStudentRepository())
    school_service = FindSchoolById(PostgresSchoolRepository())
    category_service = PostgresCategoryRepository()

    # Crear caso de uso
    usecase = GetStudentInscriptionsByCategory(
        inscription_repo,
        student_service,
        school_service,
        category_service
    )

    # Ejecutar y devolver el resultado
    return usecase.execute(event_id)


if __name__ == "__main__":
    with app.app_context():
        event_id = 1  # ID de evento a probar
        print(f"Buscando estudiantes inscritos por categoría para el evento {event_id}:")
        grouped = test_get_students_by_event_by_category(event_id)
        if not grouped:
            print("No se encontraron inscripciones para el evento.")
        else:
            # Imprime JSON completo
            print(json.dumps(grouped, indent=4, ensure_ascii=False))

            # Ejemplo de recorrido simplificado
            for cat_name, cat_info in grouped.items():
                print(f"Categoría: {cat_name} (ID: {cat_info['id']})")
                for student in cat_info['students']:
                    print(
                        f"  - {student['last_name']}, {student['first_name']} "
                        f"| Colegio: {student['school_name']} | Departamento: {student['department']} "
                        f"| Provincia: {student['province']}"
                    )
