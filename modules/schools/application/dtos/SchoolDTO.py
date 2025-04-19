# modules/schools/application/dtos/SchoolDTO.py
from pydantic import BaseModel, field_validator
from typing import Optional, List

from modules.schools.domain.School import School


class SchoolDTO(BaseModel):
    id: Optional[int] = None
    name: str

    @field_validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("School name cannot be empty")
        return v.strip()

    @classmethod
    def from_domain(cls, school: School):
        return cls(
            id=school.id,
            name=school.name,
        )

    def to_domain(self) -> School:

        return School(
            id=self.id,
            name=self.name,
        )