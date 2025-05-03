from modules.groups.application.dtos.GroupsDTO import GroupsDTO
from modules.groups.domain.GroupRepository import GroupRepository


class FindGroupsOfTutorInDelegation:
    def __init__(self, repository: GroupRepository):
        self.__repository = repository


    def execute(self,delegation_id: int, tutor_id: int):
        groups = self.__repository.get_groups_by_tutor_and_delegation(tutor_id, delegation_id)
        return GroupsDTO.from_groups(groups)