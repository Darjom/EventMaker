from .dtos.GroupDTO import GroupDTO
from ..domain.GroupRepository import GroupRepository


class GroupCreator:
    def __init__(self, repository: GroupRepository):
        self.repository = repository

    def execute(self, group_dto: GroupDTO) -> GroupDTO:
        group = group_dto.to_domain()
        saved_group = self.repository.save(group)
        return GroupDTO.from_domain(saved_group)