from typing import List
from pydantic import BaseModel
from .GroupDTO import GroupDTO
from ...domain.Group import Group


class GroupsDTO(BaseModel):
    groups: List[GroupDTO]

    @classmethod
    def from_domain_list(cls, groups: List[Group]):
        return cls(
            groups=[GroupDTO.from_domain(group) for group in groups]
        )

