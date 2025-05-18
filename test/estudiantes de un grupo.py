from app import app
from modules.groups.application.GetStudentsOfGroup import GetStudentsOfGroup
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository


def test_get_students_of_group():
    # ID del grupo a probar (asegúrate que exista en tu base de datos)
    grupo_id = 1

    # Inicializar repositorio
    group_repository = PostgresGroupRepository()

    # Inicializar caso de uso
    get_students = GetStudentsOfGroup(group_repo=group_repository)

    # Ejecutar el caso de uso
    students = get_students.execute(grupo_id)

    # Imprimir los resultados
    print(f"Estudiantes del grupo {grupo_id}:")
    for student in students:
        print(f"ID: {student.id}, Nombre: {student.first_name} {student.last_name}")

    return students


if __name__ == "__main__":
    with app.app_context():  # Activar el contexto de la aplicación
        test_get_students_of_group()
