from app import app
from modules.delegations.application.GetStudentByDelegation import GetStudentIdsByDelegation
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.students.application.GetStudentsByListIds import GetStudentsByListIds

from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

from modules.tutors.application.GetStudentsUnderTutorship import GetStudentsUnderTutorship


def test_list_students_by_delegacion(delegacion_id: int):
    # Repositorios
    delegacion_repository = PostgresDelegationRepository()
    student_repository = PostgresStudentRepository()

    # Servicios
    get_students_service =GetStudentIdsByDelegation(delegacion_repository)
    list_students_service =GetStudentsByListIds(student_repository)

    # Paso 1: Obtener lista de IDs de estudiantes bajo tutoría
    student_ids = get_students_service.execute(delegation_id=delegacion_id)
    print(f"\nEstudiantes asignados a la delegacion con ID {delegacion_id}:")
    print(student_ids)

    # Paso 2: Obtener información detallada de cada estudiante
    students_dto = list_students_service.execute(student_ids)

    print("\n=== Detalles de los estudiantes ===")
    for student in students_dto.students:
        print(f"- ID: {student.id}")
        print(f"  Nombre: {student.first_name} {student.last_name}")
        print(f"  Email: {student.email}")
        print(f"  Curso: {student.course}")
        print(f"  Departamento: {student.department}")
        print(f"  Provincia: {student.province}")
        print("---")

# Activador del test
if __name__ == "__main__":
    with app.app_context():
        print("=== Prueba: estudiantes bajo tutoría ===")
        delegacion = 1  # Cambia esto por el ID que desees probar
        test_list_students_by_delegacion(delegacion_id = delegacion)