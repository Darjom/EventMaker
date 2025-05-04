from modules.delegations.domain.DelegationRepository import DelegationRepository
from modules.tutors.application.GetTutorsByListIds import GetTutorsByListIds
from modules.tutors.domain.TutorRepository import TutorRepository


class GetTutorsByDelegation:
    def __init__(self, delegation_repository: DelegationRepository, tutor_repository: TutorRepository):
        self.__delegation_repository = delegation_repository
        self.__tutor_repository = tutor_repository

    def execute(self, delegation_id: int):
        list_ids = self.__delegation_repository.get_tutor_ids_by_delegation_id(delegation_id)
        tutors = GetTutorsByListIds(self.__tutor_repository).execute(list_ids)
        return tutors
