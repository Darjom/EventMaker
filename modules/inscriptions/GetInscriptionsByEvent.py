from typing import Dict, Any, List, Optional

from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.application.GetStudentById import GetStudentById


class GetInscriptionsByEvent:
    def __init__(
        self,
        inscription_repo: InscriptionRepository,
        student_service: GetStudentById,
        area_service: AreaRepository,
        category_service: CategoryRepository
    ):
        self.inscription_repo = inscription_repo
        self.student_service = student_service
        self.area_service = area_service
        self.category_service = category_service

    def execute(self, event_id: int) -> Dict[str, Any]:
        """
        Construye un diccionario de inscripciones para un evento, agrupado
        por área y categoría, incluyendo IDs y nombres.
        :param event_id: Identificador del evento
        :return: Diccionario jerárquico de inscripciones
        """
        inscriptions = self._fetch_inscriptions(event_id)
        return self._group_by_area_and_category(inscriptions)

    def _fetch_inscriptions(self, event_id: int) -> List:
        """
        Obtiene la lista de Inscription desde el repositorio.
        """
        return self.inscription_repo.find_by_id_event(event_id) or []

    def _group_by_area_and_category(self, inscriptions: List) -> Dict[str, Any]:
        """
        Agrupa la lista de inscripciones primero por área, luego por categoría.
        """
        result: Dict[str, Any] = {}
        for insc in inscriptions:
            area_id, area_name = self._get_area_info(insc.area_id)
            cat_id, cat_name, _price = self._get_category_info(insc.category_id)

            # Inicializar estructura para el área
            area_entry = result.setdefault(
                area_name,
                {"id": area_id, "categories": {}}
            )

            # Inicializar estructura para la categoría
            categories = area_entry["categories"]
            cat_entry = categories.setdefault(
                cat_name,
                {"id": cat_id, "inscriptions": []}
            )

            # Añadir inscripción formateada
            cat_entry["inscriptions"].append(
                self._build_entry(insc, area_id, cat_id)
            )

        return result

    def _get_area_info(self, area_id: int) -> (int, str):
        """
        Recupera ID y nombre de un área.
        """
        area = self.area_service.find_by_id(area_id)
        if not area:
            raise ValueError(f"Área con ID {area_id} no encontrada")
        return area.id_area, area.nombre_area

    def _get_category_info(self, category_id: int) -> (int, str, float):
        """
        Recupera ID, nombre y precio de una categoría.
        """
        category = self.category_service.find_by_id(category_id)
        if not category:
            raise ValueError(f"Categoría con ID {category_id} no encontrada")
        return category.category_id, category.category_name, category.price

    def _build_entry(
        self,
        insc,
        area_id: int,
        category_id: int
    ) -> Dict[str, Any]:
        """
        Construye el dict de una inscripción, con IDs y nombres.
        """
        student_dto = self.student_service.execute(insc.student_id)
        if student_dto is None:
            student_name = "Desconocido"
            course = None
        else:
            student_name = student_dto.name
            course = getattr(student_dto, 'course', None)

        return {
            "area_id": area_id,
            "category_id": category_id,
            "student_id": insc.student_id,
            "student_name": student_name,
            "course": course,
            "status": insc.status,
            "inscription_date": insc.inscription_date.isoformat()
        }
