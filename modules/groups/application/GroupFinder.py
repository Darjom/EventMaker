# modules/groups/application/GroupFinder.py

from modules.groups.domain.GroupRepository import GroupRepository
from modules.groups.application.dtos.GroupDTO import GroupDTO

class GroupFinder:
    def __init__(self, repository: GroupRepository):
        self.repository = repository

    def execute(self, group_id: int) -> GroupDTO:
        group = self.repository.find_by_id(group_id)
        if not group:
            raise ValueError("Grupo no encontrado")
        return GroupDTO.from_domain(group)
