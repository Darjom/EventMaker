from modules.delegations.domain.DelegationTutorRepository import DelegationTutorRepository
from modules.groups.application.dtos.GroupsDTO import GroupsDTO
from modules.groups.domain.GroupRepository import GroupRepository
from modules.user.application.GetUserById import GetUserById
from modules.user.domain.UserRepository import UserRepository


class FindGroupsOfTutorInDelegation:
    USER_NOT_FOUND = 0
    USER_NOT_MASTER = 1

    def __init__(self, repository: GroupRepository,
                 delegationTutor_repository: DelegationTutorRepository,
                 repository_user: UserRepository):
        self.__repository = repository
        self.__delegationTutor_repository = delegationTutor_repository
        self.__repository_user = repository_user

    def execute(self, delegation_id: int, tutor_id: int):
        tutor = GetUserById(self.__repository_user).execute(tutor_id)

        if tutor is None:
            return self.USER_NOT_FOUND

        role_name = self.__delegationTutor_repository.get_role_name_by_tutor_and_delegation(tutor_id, delegation_id)

        if role_name != "master":
            groups = self.__repository.get_groups_by_tutor_and_delegation(tutor_id, delegation_id)
        else:
            groups = self.__repository.find_by_delegation(delegation_id)

        return GroupsDTO.from_groups(groups)
