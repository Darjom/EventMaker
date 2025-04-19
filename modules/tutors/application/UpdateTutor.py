from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.domain.TutorRepository import TutorRepository


class UpdateTutor:
    def __init__(self,repository: TutorRepository):
        self.repository = repository

    def execute(self,tutor_dto: TutorDTO) -> TutorDTO:

        tutor = self.repository.update(tutor_dto.to_domain())
        return TutorDTO.from_domain(tutor)