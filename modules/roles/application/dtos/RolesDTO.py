from typing import List
from pydantic import BaseModel
from .RoleDTO import RoleDTO

class RolesDTO(BaseModel):
    roles: List[RoleDTO]

    @classmethod
    def from_domain_list(cls, roles: list):
        return cls(
            eventos=[RoleDTO.fromDomain(role) for role in roles]
        )