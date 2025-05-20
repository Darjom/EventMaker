from pydantic import BaseModel
from typing import Optional, List
from modules.roles.domain.Rol import Rol  # Entidad de dominio

class RoleDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    permissions: Optional[List[str]] = None

    @classmethod
    def fromDomain(cls, role: Rol) -> "RoleDTO":
        return cls(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=role.permissions
        )

    def toDomain(self) -> Rol:
        return Rol(
            id=self.id,
            name=self.name,
            description=self.description,
            permissions=self.permissions
        )
    