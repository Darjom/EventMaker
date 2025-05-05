from app import app
from modules.delegations.application.AssignStudentToDelegationByEmail import AssignStudentToDelegationByEmail
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository

from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository


def test_assign_student_to_delegation_by_email():
    # Email de prueba y delegación de prueba (deben existir)
    email = "jjquiquegfk@example.com"
    delegation_id = 1  # Asegúrate de que esta delegación exista en tu base de datos

    # Inicializar repositorios
    user_repository = PostgresUserRepository()
    delegation_repository = PostgresDelegationRepository()

    # Inicializar el caso de uso
    assign_service = AssignStudentToDelegationByEmail(delegation_repository, user_repository)

    # Ejecutar el servicio
    return assign_service.execute(delegation_id, email)


if __name__ == "__main__":
    with app.app_context():
        result = test_assign_student_to_delegation_by_email()

        if result == 0:
            print("❌ Usuario con ese correo no existe.")
        elif result == 1:
            print("✅ Estudiante asignado exitosamente a la delegación.")
        elif result == 2:
            print("⚠️ El estudiante ya pertenece a esa delegación.")
        elif result == 3:
            print("🚫 El usuario no tiene el rol de estudiante.")
        else:
            print("❓ Resultado inesperado:", result)
