from pydantic import BaseModel, field_validator
from datetime import date, time
from typing import Optional

from modules.inscriptions.domain.Inscription import Inscription


class InscriptionDTO(BaseModel):
    student_id: int
    event_id: int
    area_id: int
    category_id: int
    inscription_date: date = None
    status: str = None
    id: Optional[str] = None  # ID compuesto generado
    delegation_id: Optional[int] = None
    voucher_id: Optional[int] = None

    @field_validator('status')
    def validate_status(cls, v):
        valid_statuses = ['Pendiente', 'Confirmado']
        if v not in valid_statuses:
            raise ValueError(f"Invalid status. Allowed values: {', '.join(valid_statuses)}")
        return v

    @classmethod
    def from_domain(cls, inscription) -> 'InscriptionDTO':
        return cls(
            student_id=inscription.student_id,
            event_id=inscription.event_id,
            area_id=inscription.area_id,
            category_id=inscription.category_id,
            inscription_date=inscription.inscription_date,
            status=inscription.status,
            id=f"{inscription.student_id}-{inscription.event_id}-{inscription.area_id}-{inscription.category_id}",
            delegation_id=inscription.delegation_id,
            voucher_id=inscription.voucher_id
        )

    def to_domain(self):

        return Inscription(
            student_id=self.student_id,
            event_id=self.event_id,
            area_id=self.area_id,
            category_id=self.category_id,
            delegation_id=self.delegation_id,
            voucher_id=self.voucher_id,
            inscription_date=self.inscription_date,
            status=self.status
        )