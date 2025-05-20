from datetime import datetime, date
from zoneinfo import ZoneInfo

from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.domain.StudentRepository import StudentRepository
from modules.events.domain.EventRepository import EventRepository
from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository


class InscriptionRegistrar:
    def __init__(
            self,
            inscription_repository: InscriptionRepository,
            student_repository: StudentRepository,
            event_repository: EventRepository,
            area_repository: AreaRepository,
            category_repository: CategoryRepository
    ):
        self.inscription_repo = inscription_repository
        self.student_repo = student_repository
        self.event_repo = event_repository
        self.area_repo = area_repository
        self.category_repo = category_repository

    def execute(self, inscription_dto: InscriptionDTO) -> InscriptionDTO:

        inscription_dto.inscription_date = date.today()
        inscription_dto.status = "Pendiente"

        student = self.student_repo.find_by_id(inscription_dto.student_id)
        if not student:
            raise ValueError("Student does not exist")

        event = self.event_repo.find_by_id(inscription_dto.event_id)
        if not event:
            raise ValueError("Event does not exist")

        area = self.area_repo.find_by_id(inscription_dto.area_id)
        if not area:
            raise ValueError("Area does not exist")

        category = self.category_repo.find_by_id(inscription_dto.category_id)
        if not category:
            raise ValueError("Category does not exist")

        existing = self.inscription_repo.find_by_ids(
            inscription_dto.student_id,
            inscription_dto.event_id,
            inscription_dto.area_id,
            inscription_dto.category_id
        )
        if existing:
            raise ValueError("Inscription already exists")

        inscription = inscription_dto.to_domain()
        saved_inscription = self.inscription_repo.save(inscription)

        return InscriptionDTO.from_domain(saved_inscription)
