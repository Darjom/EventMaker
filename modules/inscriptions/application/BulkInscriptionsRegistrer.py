from datetime import date
from typing import List

from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.domain.StudentRepository import StudentRepository


class BulkInscriptionsRegistrar:
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

    def execute(
        self,
        students_ids: List[int],
        event_id: int,
        area_id: int,
        category_id: int,
        delegation_id: int
    ) -> None:
        if not students_ids:
            raise ValueError("The list of student IDs is empty")

        for student_id in students_ids:
            inscription_dto = InscriptionDTO(
                student_id=student_id,
                event_id=event_id,
                area_id=area_id,
                category_id=category_id,
                inscription_date=date.today(),
                status="Pendiente",
                delegation_id=delegation_id
            )
            self.inscription_individual(inscription_dto)

    def inscription_individual(self, inscription_dto: InscriptionDTO) -> InscriptionDTO:
        print("🔍 Validando estudiante...")
        student = self.student_repo.find_by_id(inscription_dto.student_id)
        print(f"Student: {student}")
        if not student:
            raise ValueError("Student does not exist")

        print("🔍 Validando evento...")
        event = self.event_repo.find_by_id(inscription_dto.event_id)
        print(f"Event: {event}")
        if not event:
            raise ValueError("Event does not exist")

        print("🔍 Validando área...")
        area = self.area_repo.find_by_id(inscription_dto.area_id)
        print(f"Area: {area}")
        if not area:
            raise ValueError("Area does not exist")

        print("🔍 Validando categoría...")
        category = self.category_repo.find_by_id(inscription_dto.category_id)
        print(f"Category: {category}")
        if not category:
            raise ValueError("Category does not exist")

        print("🔍 Buscando inscripción existente...")
        existing = self.inscription_repo.find_by_ids(
            inscription_dto.student_id,
            inscription_dto.event_id,
            inscription_dto.area_id,
            inscription_dto.category_id
        )
        print(f"Inscripción existente: {existing}")
        if existing:
            raise ValueError("Inscription already exists")

        print("✅ Guardando inscripción...")
        inscription = inscription_dto.to_domain()
        saved_inscription = self.inscription_repo.save(inscription)

        print("✅ Inscripción guardada:", saved_inscription)
        return InscriptionDTO.from_domain(saved_inscription)
