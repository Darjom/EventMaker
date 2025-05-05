from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from modules.tutors.domain.Tutor import Tutor


class TutorDTO(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: str = ""
    email: str = ""
    password: str = ""
    active: bool = False
    confirmed_at: Optional[datetime] = None
    fs_uniquifier: Optional[str] = None
    ci: str = ""
    expedito_ci: str = ""
    fecha_nacimiento: Optional[datetime] = None
    roles: Optional[List[str]] = None


    @classmethod
    def from_domain(cls, tutor: Tutor):
        return cls(
            id=tutor.id,
            first_name=tutor.first_name,
            last_name=tutor.last_name,
            email=tutor.email,
            password=tutor.password,
            active=tutor.active,
            confirmed_at=tutor.confirmed_at,
            fs_uniquifier=tutor.fs_uniquifier,
            ci=tutor.ci,
            expedito_ci=tutor.expedito_ci,
            fecha_nacimiento=tutor.fecha_nacimiento,
            roles=tutor.roles
        )

    def to_domain(self) -> Tutor:
        """
        Convierte el DTO TutorDTO en un objeto de dominio tutor.
        """
        return Tutor(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            active=self.active,
            confirmed_at=self.confirmed_at,
            fs_uniquifier=self.fs_uniquifier,
            ci =self.ci,
            expedito_ci=self.expedito_ci,
            fecha_nacimiento=self.fecha_nacimiento,
            roles=self.roles
        )

