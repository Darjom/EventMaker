from app import app
from modules.user.application.UserCreator import UserCreator
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.roles.application.RoleQueryService import RoleQueryService


def test_create_user():
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
        role_ids=[2],  # Asegúrate que exista este rol en tu DB
        first_name="dan",
        last_name="Reque",
        email="mod@modmod.com",
        password="12345678"
    )

#adm@adm.com - admin
#mod@modmod.com - moderador
if __name__ == "__main__":
    with app.app_context():
        # Crear el usuario
        created_user = test_create_user()
        print(f"Usuario creado: ID={created_user.id}")
        print(f"Detalles: {created_user}")