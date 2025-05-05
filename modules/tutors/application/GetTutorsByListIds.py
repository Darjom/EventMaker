from typing import List

from modules.tutors.application.dtos.TutorsDTO import TutorsDTO
from modules.tutors.domain.TutorRepository import TutorRepository


class GetTutorsByListIds:

    def __init__(self, repository: TutorRepository):
        self.__repository = repository

    def execute(self, tutor_ids: List[int]) -> TutorsDTO:
        tutors = self.__repository.find_by_ids(tutor_ids)
        return TutorsDTO.from_domain_list(tutors)
