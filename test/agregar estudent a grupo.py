# test/group_assign_student.py

from app import app
from modules.groups.application.AssignGroupToStudent import AssignGroupToStudent
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository


def test_asignar_student_a_grupo():
    # Inicializar el repositorio
    group_repository = PostgresGroupRepository()

    # Inicializar el caso de uso
    asignador = AssignGroupToStudent(repository=group_repository)
    grupo_id = 1
    estudiante_id = 10

    # Ejecutar la asignación
    asignador.execute(grupo_id, estudiante_id)


if __name__ == "__main__":
    with app.app_context():
        test_asignar_student_a_grupo()
