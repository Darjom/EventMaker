from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.domain.TutorRepository import TutorRepository


class FindTutorById:

    def __init__(self,repository: TutorRepository):
        self.repository = repository

    def execute(self, id: int) -> TutorDTO:

        tutor = self.repository.find_by_id(id)
        return TutorDTO.from_domain(tutor)