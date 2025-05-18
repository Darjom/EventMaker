from typing import Dict, Any, List

from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.application.GetStudentById import GetStudentById
from modules.schools.application.FindSchoolById import FindSchoolById
from modules.categories.domain.CategoryRepository import CategoryRepository


class GetStudentInscriptionsByCategory:
    def __init__(
        self,
        inscription_repo: InscriptionRepository,
        student_service: GetStudentById,
        school_service: FindSchoolById,
        category_service: CategoryRepository
    ):
        self.inscription_repo = inscription_repo
        self.student_service = student_service
        self.school_service = school_service
        self.category_service = category_service

    def execute(self, event_id: int) -> Dict[str, Any]:
        """
        Devuelve un diccionario de inscripciones de un evento,
        agrupado por categoría. Para cada categoría lista los estudiantes
        con campos: last_name, first_name, school_name, department, province.
        :param event_id: ID del evento
        :return: { category_name: { id: category_id, students: [ {...} ] } }
        """
        inscriptions = self.inscription_repo.find_by_id_event(event_id) or []
        return self._group_by_category(inscriptions)

    def _group_by_category(self, inscriptions: List) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for insc in inscriptions:
            # Obtener info de categoría
            cat_id, cat_name, _price = self._get_category_info(insc.category_id)

            cat_entry = result.setdefault(
                cat_name,
                {"id": cat_id, "students": []}
            )

            # Construir datos del estudiante
            student_data = self._build_student_entry(insc.student_id)
            cat_entry["students"].append(student_data)

        return result

    def _get_category_info(self, category_id: int):
        category = self.category_service.find_by_id(category_id)
        if not category:
            raise ValueError(f"Categoría con ID {category_id} no encontrada")
        return category.category_id, category.category_name, category.price

    def _build_student_entry(self, student_id: int) -> Dict[str, Any]:
        student_dto = self.student_service.execute(student_id)
        if not student_dto:
            return {
                "last_name": None,
                "first_name": None,
                "school_name": None,
                "department": None,
                "province": None
            }

        # Obtener nombre del colegio
        school_dto = self.school_service.execute(student_dto.school_id) if student_dto.school_id else None
        school_name = school_dto.name if school_dto else None

        return {
            "last_name": student_dto.last_name,
            "first_name": student_dto.first_name,
            "school_name": school_name,
            "department": student_dto.department,
            "province": student_dto.province
        }
