from typing import List

from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository


class GetStudentInscriptionsByEvent:
    def __init__(self, repository: InscriptionRepository):
        self.__repository = repository

    def execute(self, event_id: int, student_id: int) -> List[InscriptionDTO]:
        inscriptions = self.__repository.find_by_student_and_event(student_id, event_id)
        return [InscriptionDTO.from_domain(inscription) for inscription in inscriptions]
