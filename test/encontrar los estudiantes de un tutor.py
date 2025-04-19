from app import app
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

from modules.tutors.application.GetStudentsUnderTutorship import GetStudentsUnderTutorship
from modules.students.application.ListStudentsUnderTutor import ListStudentsUnderTutor

def test_list_students_under_tutor(tutor_id: int):
    # Repositorios
    tutor_repository = PostgresTutorRepository()
    student_repository = PostgresStudentRepository()

    # Servicios
    get_students_service = GetStudentsUnderTutorship(tutor_repository)
    list_students_service = ListStudentsUnderTutor(student_repository)

    # Paso 1: Obtener lista de IDs de estudiantes bajo tutoría
    student_ids = get_students_service.execute(tutor_id)
    print(f"\nEstudiantes asignados al tutor con ID {tutor_id}:")
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
        tutor_id = 1  # Cambia esto por el ID que desees probar
        test_list_students_under_tutor(tutor_id)
