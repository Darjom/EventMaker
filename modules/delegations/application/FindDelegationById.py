from modules.delegations.application.dtos.DelegationDTO import DelegationDTO
from modules.delegations.domain.DelegationRepository import DelegationRepository


class FindDelegationById:
    def __init__(self, repository: DelegationRepository):
        self.__repository = repository

    def execute(self, delegation_id: int) -> DelegationDTO:
        delegation_domain = self.__repository.find_by_delegation_id(delegation_id)
        return DelegationDTO.from_domain(delegation_domain)