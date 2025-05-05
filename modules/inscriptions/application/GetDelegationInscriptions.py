from typing import List
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository


class GetDelegationInscriptions:
    def __init__(self, repository: InscriptionRepository):
        self.__repository = repository

    def execute(self, delegation_id: int) -> List[InscriptionDTO]:
        inscriptions = self.__repository.find_by_delegation_id(delegation_id)
        return [InscriptionDTO.from_domain(inscription) for inscription in inscriptions]
