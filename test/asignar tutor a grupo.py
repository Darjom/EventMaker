# test/group_create.py

from app import app
from modules.groups.application.AssignGroupToTutor import AssignGroupToTutor

from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository



def test_asignar_group():
    # Inicializar repositorio
    group_repository = PostgresGroupRepository()

    # Inicializar el caso de uso
    asignador = AssignGroupToTutor(repository=group_repository)
    grupo = 1
    tutor = 10

    asignador.execute(grupo, tutor)





if __name__ == "__main__":
    with app.app_context():
        test_asignar_group()

