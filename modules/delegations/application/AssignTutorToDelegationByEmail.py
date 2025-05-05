from modules.delegations.application.DelegationTutorAssigner import DelegationTutorAssigner
from modules.delegations.application.dtos.DelegationTutorDTO import DelegationTutorDTO
from modules.delegations.domain.DelegationTutorRepository import DelegationTutorRepository
from modules.user.application.GetUserByEmail import GetUserByEmail
from modules.user.domain.UserRepository import UserRepository


class AssignTutorToDelegationByEmail:
    SUCCESS = 2
    USER_NOT_FOUND = 0
    USER_NOT_TUTOR = 1

    def __init__(self, repository: DelegationTutorRepository, repository_user: UserRepository):
        self.__repository = repository
        self.__repository_user = repository_user

    def execute(self, delegation_id: int, tutor_email: str) -> int:
        tutor = GetUserByEmail(self.__repository_user).execute(tutor_email)

        if tutor is None:
            return self.USER_NOT_FOUND

        if not isinstance(tutor.roles, list) or "tutor" not in tutor.roles:
            return self.USER_NOT_TUTOR

        role_id = 6  # id de tutor colaborador

        tutorDelegation = DelegationTutorDTO(
            delegation_id=delegation_id,
            tutor_id=tutor.id,
            role_id=role_id
        )

        DelegationTutorAssigner(self.__repository).execute(tutorDelegation)

        return self.SUCCESS
