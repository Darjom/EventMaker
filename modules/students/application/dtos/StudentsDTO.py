from typing import List
from pydantic import BaseModel

from modules.students.application.dtos.StudentDTO import StudentDTO


class StudentsDTO(BaseModel):
    students: List[StudentDTO]

    @classmethod
    def from_domain_list(cls, students: list):
        return cls(
            students=[StudentDTO.from_domain(student) for student in students]
        )