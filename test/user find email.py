from app import app
from modules.user.application.GetUserByEmail import GetUserByEmail
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository


def test_get_user_by_email():
    # Email de prueba — asegúrate de que este usuario exista en tu base de datos
    email = "danielk@example.com"

    # Inicializar el repositorio
    user_repository = PostgresUserRepository()

    # Inicializar el caso de uso
    get_user_service = GetUserByEmail(user_repository)

    # Ejecutar el servicio
    return get_user_service.execute(email)


if __name__ == "__main__":
    with app.app_context():
        user_dto = test_get_user_by_email()
        if user_dto:
            print("User found:")
            print(user_dto)
        else:
            print("User not found.")
