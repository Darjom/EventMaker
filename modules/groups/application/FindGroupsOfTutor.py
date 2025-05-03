from modules.groups.domain.GroupRepository import GroupRepository


class FindGroupsOfTutor:
    def __init__(self, repository: GroupRepository):
        self.__repository = repository


    def execute(self, tutor_id: int):
        groups = self.__repository.get_groups_by_tutor_id(tutor_id)
        return groups