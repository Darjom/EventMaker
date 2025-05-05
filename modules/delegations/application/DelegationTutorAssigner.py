from .dtos.DelegationTutorDTO import DelegationTutorDTO
from ..domain.DelegationTutorRepository import DelegationTutorRepository


class DelegationTutorAssigner:
    def __init__(self, repository: DelegationTutorRepository):
        self.repository = repository

    def execute(self, dto: DelegationTutorDTO):
        delegation_tutor = dto.to_domain()
        saved_relation = self.repository.save(delegation_tutor)
        return DelegationTutorDTO.from_domain(saved_relation)