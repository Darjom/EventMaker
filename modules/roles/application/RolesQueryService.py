from .dtos.RoleDTO import RoleDTO
from .dtos.RolesDTO import RolesDTO
from modules.roles.domain.RolesRepository import RolesRepository

class RolesQueryService:
    def __init__(self, repository: RolesRepository):
        self.repository = repository

    def execute(self) -> RolesDTO:
        roles = self.repository.find_all()
        role_dtos = [RoleDTO.fromDomain(role) for role in roles]
        return RolesDTO(roles=role_dtos)