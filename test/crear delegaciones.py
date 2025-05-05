from datetime import datetime
from app import app
from modules.delegations.application.TutorDelegationFinder import TutorDelegationsFinder
from modules.delegations.application.dtos.DelegationDTO import DelegationDTO
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.delegations.application.DelegationCreator import DelegationCreator

from modules.delegations.infrastructure.PostgresDelegationTutorRepository import PostgresDelegationTutorRepository


def test_create_delegation(tutor_id: int = 7):
    # Crear DTO de delegación de prueba
    delegation_dto = DelegationDTO(
        nombre="Delegación Ejemplo",
        evento_id=1,  # Asume que existe un evento con ID 1
        codigo="DEL-2024"
    )

    # Inicializar repositorios y servicios
    delegation_repo = PostgresDelegationRepository()
    tutor_repo = PostgresDelegationTutorRepository()
    creator = DelegationCreator(delegation_repo, tutor_repo)

    return creator.execute(delegation_dto, tutor_id)


def test_get_tutor_delegations(tutor_id: int = 7):
    # Inicializar repositorios y servicios
    delegation_repo = PostgresDelegationRepository()
    tutor_repo = PostgresDelegationTutorRepository()
    finder = TutorDelegationsFinder(delegation_repo, tutor_repo)

    return finder.execute(tutor_id)


if __name__ == "__main__":
    with app.app_context():
        # Prueba de creación
        created_delegation = test_create_delegation()
        print("Delegación creada:", created_delegation)

        # Prueba de recuperación
        tutor_delegations = test_get_tutor_delegations()
        print("\nDelegaciones del tutor:", tutor_delegations)