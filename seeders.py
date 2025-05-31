# En test/user_create.py
import sys
import os

from modules.Data.RolesAndPermissions.Seeder import seed_roles_and_permissions

# Añade el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from datetime import datetime
from modules.user.application.UserCreator import UserCreator
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.roles.application.RoleQueryService import RoleQueryService

def create_user():
    # Inicializar repositorios
    user_repository = PostgresUserRepository()
    role_repository = PostgresRolesRepository()
    role_query_service = RoleQueryService(role_repository)

    # Inicializar creador de usuarios
    creator = UserCreator(
        user_repo=user_repository,
        role_query_service=role_query_service
    )

    # Ejecutar creación de usuario
    return creator.execute(
        role_ids=[1],  # Asegúrate que exista este rol en tu DB
        first_name="admin",
        last_name="Administrativo",
        email="admin@admin.com",
        password="fdAp62-}+#W9",
        ci="",
        expedito_ci="",
        fecha_nacimiento=datetime(2025, 5, 20, 9, 0, 0),
    )

def create_roles_and_permissions():

    # Inserta datos de roles y permisos
    seed_roles_and_permissions()

def create_schools():
    # cargar colegios
    from modules.Data.DatosColegios.cargar_colegios import CargarColegios
    cargador = CargarColegios()
    cargador.main()



if __name__ == "__main__":
    with app.app_context():

        # Crear el usuario
        created_user = create_user()
        create_roles_and_permissions()
        create_schools()

