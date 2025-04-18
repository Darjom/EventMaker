from modules.tutors.domain.TutorRepository import TutorRepository


class TutorStudentAssigner:
    def __init__(self, repository: TutorRepository):
        self.repository = repository

    def execute(self, student_id: int, tutor_id: int):
        return self.repository.assign_tutorship(student_id, tutor_id)

