# test_role_services.py
from app import app
from modules.roles.application.RolesQueryService import RolesQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.roles.application.RoleQueryService import RoleQueryService



def test_find_role_by_id(role_id: int):
    """Prueba obtener un rol por su ID"""
    repo = PostgresRolesRepository()
    query_service = RoleQueryService(repo)

    result = query_service.execute(role_id)

    print(f"\nRol encontrado con ID {role_id}:")
    if result:
        print(f"- Nombre: {result.name}")
        print(f"- Descripción: {result.description}")
        print(f"- Permisos: {', '.join(result.permissions) if result.permissions else 'Ninguno'}")
    else:
        print("⚠️ Rol no encontrado")
    return result


def test_find_all_roles():
    """Prueba obtener todos los roles"""
    repo = PostgresRolesRepository()
    query_service = RolesQueryService(repo)

    result = query_service.execute()

    print("\nTodos los roles:")
    for role in result.roles:
        print(f"- {role.name} (ID: {role.id}) - Permisos: {len(role.permissions)}")
    return result


if __name__ == "__main__":
    with app.app_context():
        # Testear ambos servicios
        test_find_role_by_id(10)  # Probamos con ID 1
        test_find_all_roles()