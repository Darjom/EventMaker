from .dtos.RoleDTO import RoleDTO
from .dtos.RolesDTO import RolesDTO
from modules.roles.domain.RolesRepository import RolesRepository

class RolesQueryService:
    def __init__(self, repository: RolesRepository):
        self.repository = repository

    def execute(self) -> RolesDTO:
        roles = self.repository.find_all()
        role_dtos = [RoleDTO.fromDomain(role) for role in roles]

        # Filtrar y eliminar los roles con nombre "master" o "colaborador"
        role_dtos = [
            role_dto for role_dto in role_dtos
            if role_dto.name not in ("master", "colaborador")
        ]

        return RolesDTO(roles=role_dtos)