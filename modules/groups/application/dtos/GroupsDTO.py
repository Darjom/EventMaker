from typing import List
from pydantic import BaseModel
from .GroupDTO import GroupDTO


class GroupsDTO(BaseModel):
    grupos: List[GroupDTO]

    def get_grupos(self):
        return self.grupos