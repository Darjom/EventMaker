from .dtos.RoleDTO import RoleDTO
from modules.roles.domain.RolesRepository import RolesRepository


class RoleQueryService:
    def __init__(self, repository: RolesRepository):
        self.repository = repository  # Inyección del repositorio

    def execute(self, role_id: int) -> RoleDTO:
        # Buscar el rol por ID usando el repositorio
        role = self.repository.find_by_id(role_id)

        if not role:
            return None  # O lanzar una excepción: raise ValueError("Rol no encontrado")

        return RoleDTO.fromDomain(role)