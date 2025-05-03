from modules.delegations.application.dtos.DelegationDTO import DelegationDTO
from modules.delegations.domain.DelegationRepository import DelegationRepository


class FindDelegationByCode:
    def __init__(self, repository: DelegationRepository):
        self.__repository = repository

    def execute(self, code: str) -> DelegationDTO:
        delegation_domain = self.__repository.find_by_code(code)
        return DelegationDTO.from_domain(delegation_domain)