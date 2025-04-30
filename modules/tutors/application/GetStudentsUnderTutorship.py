from typing import List

from modules.tutors.domain.TutorRepository import TutorRepository


class GetStudentsUnderTutorship:

    def __init__(self, repository: TutorRepository):
        self.__repository = repository

    def execute(self, tutor_id: int) -> List[int]:
        students_ids = self.__repository.find_students(tutor_id)
        return students_ids

