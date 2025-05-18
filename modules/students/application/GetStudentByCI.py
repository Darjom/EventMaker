from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.domain.StudentRepository import StudentRepository


class GetStudentByCI:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, user_ci: str) -> StudentDTO | None:
        user = self.repository.find_by_ci(user_ci)
        if user is None:
            return None
        return StudentDTO.from_domain(user)
