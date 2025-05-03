from typing import List
from pydantic import BaseModel
from .GroupDTO import GroupDTO
from ...domain.Group import Group



class GroupsDTO(BaseModel):

    grupos: List[GroupDTO]

    @classmethod
    def from_domain_list(cls, groups: List[Group]):
        return cls(
            students=[GroupDTO.from_domain(group) for group in groups]
        )