from pydantic import BaseModel, field_validator
from typing import Optional

from modules.delegations.domain.Delegation import Delegation


class DelegationDTO(BaseModel):
    id_delegacion: Optional[int] = None
    nombre: Optional[str] = None
    evento_id: Optional[int] = None
    codigo: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        return value.strip()

    @classmethod
    def from_domain(cls, delegation):
        return cls(
            id_delegacion=delegation.id_delegacion,
            nombre=delegation.nombre,
            evento_id=delegation.evento_id,
            codigo=delegation.codigo
        )

    def to_domain(self):
        return Delegation(
            id_delegacion=self.id_delegacion,
            nombre=self.nombre,
            evento_id=self.evento_id,
            codigo=self.codigo
        )