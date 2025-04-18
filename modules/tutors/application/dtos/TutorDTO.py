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
    roles: Optional[List[int]] = None

    @classmethod
    def from_domain(cls, student: Tutor):
        print("tutor domain")
        print(student.ci)
        print(student.expedito_ci)

        """
        Convierte un objeto de dominio Tutor a un DTO TutorDTO.
        """
        return cls(
            id=student.id,
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            password=student.password,
            active=student.active,
            confirmed_at=student.confirmed_at,
            fs_uniquifier=student.fs_uniquifier,
            ci=student.ci,
            expedito_ci=student.expedito_ci,
            fecha_nacimiento=student.fecha_nacimiento,
            roles=student.roles
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

