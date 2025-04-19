from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from modules.students.domain.Student import Student


class StudentDTO(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: str = ""
    email: str = ""
    password: str = ""
    active: bool = False
    confirmed_at: Optional[datetime] = None
    fs_uniquifier: Optional[str] = None
    ci: str = "",
    expedito_ci: str = "",
    fecha_nacimiento: Optional[datetime] = None
    phone_number: Optional[int] = None
    school_id: Optional[int] = None
    course: str = ""
    department: str = ""
    province: str = ""
    roles: Optional[List[int]] = None

    @classmethod
    def from_domain(cls, student: Student):
        """
        Convierte un objeto de dominio Student a un DTO StudentDTO.
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
            phone_number=student.phone_number,
            school_id=student.school_id,
            course=student.course,
            department=student.department,
            province=student.province,
            roles=student.roles
        )

    def to_domain(self) -> Student:
        """
        Convierte el DTO StudentDTO en un objeto de dominio Student.
        """
        return Student(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            active=self.active,
            confirmed_at=self.confirmed_at,
            fs_uniquifier=self.fs_uniquifier,
            phone_number=self.phone_number,
            ci =self.ci,
            expedito_ci=self.expedito_ci,
            fecha_nacimiento=self.fecha_nacimiento,
            school_id=self.school_id,
            course=self.course,
            department=self.department,
            province=self.province,
            roles=self.roles
        )

