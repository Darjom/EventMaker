from .dtos.DelegationDTO import DelegationDTO
from .dtos.DelegationTutorDTO import DelegationTutorDTO
from ..domain.DelegationRepository import DelegationRepository
from ..domain.DelegationTutorRepository import DelegationTutorRepository


class DelegationCreator:
    def __init__(self, repository: DelegationRepository, repo: DelegationTutorRepository):
        self.repository = repository
        self.repo = repo

    def execute(self, delegation_dto: DelegationDTO, tutor_id: int) -> DelegationDTO:
        # Validación adicional si es necesaria
        delegation = delegation_dto.to_domain()
        saved_delegation = self.repository.save(delegation)

        #guardamos con el tutor y le damos el rol de tutor master
        delegationTutor = DelegationTutorDTO(delegation_id=saved_delegation.id_delegacion, tutor_id=tutor_id, role_id=5)
        delegationTutor_saved = self.repo.save(delegationTutor)

        return DelegationDTO.from_domain(saved_delegation)