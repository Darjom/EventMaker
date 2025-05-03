from typing import List
from pydantic import BaseModel


from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.domain.Tutor import Tutor


class TutorsDTO(BaseModel):
    tutors: List[TutorDTO]

    @classmethod
    def from_domain_list(cls, tutors: List[Tutor]):
        return cls(
            tutors=[TutorDTO.from_domain(tutor) for tutor in tutors]
        )