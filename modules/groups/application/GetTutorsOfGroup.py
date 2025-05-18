from modules.groups.domain.GroupRepository import GroupRepository


class GetTutorsOfGroup:
    def __init__(self, group_repo: GroupRepository):
        self._group_repo = group_repo

    def execute(self, grupo_id: int):
        return self._group_repo.get_tutors_by_group_id(grupo_id)



