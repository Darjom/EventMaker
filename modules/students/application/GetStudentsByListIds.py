from typing import List

from modules.students.application.dtos.StudentsDTO import StudentsDTO
from modules.students.domain.StudentRepository import StudentRepository


class GetStudentsByListIds:

    def __init__(self, repository: StudentRepository):
        self.__repository = repository

    def execute(self, students_ids: List[int]) -> StudentsDTO:

        students = self.__repository.find_students_by_list_id(students_ids)
        return StudentsDTO.from_domain_list(students)
