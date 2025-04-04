from typing import Optional, List
from modules.roles.domain.Rol import Rol
from modules.roles.domain.RolesRepository import RolesRepository
from modules.roles.infrastructure.persistence.RolMapping import RolMapping

class PostgresRolesRepository(RolesRepository):

    def __init__(self):
        pass

    def save(self, role: Rol) -> None:

        role_mapping = RolMapping.from_domain(role)
        role_mapping.add(role_mapping)
        role_mapping.commit()
        role_mapping.flush()

    def find_by_id(self, role_id: int) -> Optional[Rol]:
        role_mapping = RolMapping.query.get(role_id)
        return role_mapping.to_domain() if role_mapping else None

    def find_all(self) -> List[Rol]:
        roles_mapping = RolMapping.query.all()
        return [role.to_domain() for role in roles_mapping]
