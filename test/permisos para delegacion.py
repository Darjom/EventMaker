from app import app
from modules.tutors.application.GetTutorPermissionsInDelegation import GetTutorPermissionsInDelegation
from modules.delegations.infrastructure.PostgresDelegationTutorRepository import PostgresDelegationTutorRepository

def test_get_tutor_permissions_in_delegation(tutor_id: int = 10, delegation_id: int = 3):
    # Inicializar repositorio y servicio
    tutor_repo = PostgresDelegationTutorRepository()
    service = GetTutorPermissionsInDelegation(tutor_repo)

    # Ejecutar el caso de uso
    permissions = service.execute(tutor_id, delegation_id)

    return permissions


if __name__ == "__main__":
    with app.app_context():
        tutor_permissions = test_get_tutor_permissions_in_delegation()
        print("\nPermisos del tutor en la delegación:", tutor_permissions)
