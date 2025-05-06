from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.domain.StudentRepository import StudentRepository



class GetStudentById:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, user_id: int) -> StudentDTO | None:
        user = self.repository.find_by_id(user_id)
        if user is None:
            return None
        return StudentDTO.from_domain(user)