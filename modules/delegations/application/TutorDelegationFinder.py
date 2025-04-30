from typing import List

from .dtos.DelegationDTO import DelegationDTO
from ..domain.DelegationRepository import DelegationRepository
from ..domain.DelegationTutorRepository import DelegationTutorRepository


class TutorDelegationsFinder:
    def __init__(
            self,
            delegation_repo: DelegationRepository,
            relation_repo: DelegationTutorRepository
    ):
        self.delegation_repo = delegation_repo
        self.relation_repo = relation_repo

    def execute(self, tutor_id: int) -> List[DelegationDTO]:
        # 1. Obtener todas las relaciones del tutor
        relations = self.relation_repo.find_by_tutor(tutor_id)

        if not relations:
            return []

        # 2. Extraer los IDs de delegación
        delegation_ids = [r.delegation_id for r in relations]

        # 3. Obtener las delegaciones completas
        delegations = self.delegation_repo.find_by_ids(delegation_ids)

        # 4. Mapear a DTOs con información del rol
        return [
            DelegationDTO.from_domain(delegation).model_dump()
            for delegation in delegations
        ]