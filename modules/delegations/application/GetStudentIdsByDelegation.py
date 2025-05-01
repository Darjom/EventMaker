from modules.delegations.domain.DelegationRepository import DelegationRepository


class GetStudentIdsByDelegation:

    def __init__(self, repository: DelegationRepository):
        self.__repository = repository

    def execute(self, delegation_id: int):
        list_ids = self.__repository.get_student_ids_by_delegation_id(delegation_id)
        return list_ids