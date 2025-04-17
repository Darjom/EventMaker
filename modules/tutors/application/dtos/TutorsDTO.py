from typing import List
from pydantic import BaseModel


from modules.tutors.application.dtos.TutorDTO import TutorDTO


class StudentsDTO(BaseModel):
    tutors: List[TutorDTO]

    @classmethod
    def from_domain_list(cls, tutors: list):
        return cls(
            students=[TutorDTO.from_domain(tutor) for tutor in tutors]
        )