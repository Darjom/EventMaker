# test/group_create.py
# En test/user_create.py
import sys
import os

# Añade el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from modules.groups.application.GroupCreator import GroupCreator
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.groups.application.dtos.GroupDTO import GroupDTO


def test_create_group():
    # Inicializar repositorio
    group_repository = PostgresGroupRepository()

    # Inicializar el caso de uso
    creator = GroupCreator(repository=group_repository)

    # Crear el DTO del grupo
    group_dto = GroupDTO(
        nombre_grupo="Grupo Ciencias 2025",
        id_area=1,           # Asegúrate de que el área con id=1 exista
        id_delegacion=1      # Asegúrate de que la delegación con id=1 exista
    )

    # Ejecutar la creación
    created_group = creator.execute(group_dto)

    return created_group


if __name__ == "__main__":
    with app.app_context():
        group = test_create_group()
        print(f"Grupo creado: ID={group.id_grupo}")
        print(f"Nombre: {group.nombre_grupo}, Área: {group.id_area}, Delegación: {group.id_delegacion}")
