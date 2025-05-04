from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.domain.Inscription import Inscription
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.domain.StudentRepository import StudentRepository
from typing import List, Tuple


class GetAllStudentInscriptions:

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

    def execute(self, student_id: int):
        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError("St    udent does not exist")

        print("🔍 Buscando inscripción existente...")
        inscriptions = self.inscription_repo.find_by_id_student(student_id)

        # Si no hay inscripciones (None o lista vacía), devuelvo lista vacía
        if not inscriptions:
            return []

        # Si sí hay inscripciones, las agrupo
        return self.__group_inscriptions_by_event(inscriptions)

    def __group_inscriptions_by_event(self, inscriptions: List[Inscription]) -> List[dict]:
        """
        Agrupa las inscripciones por evento y devuelve una lista de diccionarios
        con la estructura deseada.
        """
        grouped_result = []

        while inscriptions:
            # Extraer grupo del siguiente evento
            group, inscriptions = self.__extract_next_event_group(inscriptions)

            if not group:
                break

            # Obtener info del evento
            event_id, event_name = self.__nameAndIdEvent(group[0].event_id)

            # Crear lista de inscripciones para este evento
            inscription_items = []
            for ins in group:
                area_id, area_name = self.__nameAndIdArea(ins.area_id)
                category_id, category_name = self.__nameAndIdCategory(ins.category_id)

                inscription_items.append({
                    "area_id": area_id,
                    "area_name": area_name,
                    "category_id": category_id,
                    "category_name": category_name,
                    "inscription_date": ins.inscription_date.isoformat() if ins.inscription_date else None,
                    "status": ins.status
                })

            grouped_result.append({
                "event_id": event_id,
                "event_name": event_name,
                "inscriptions": inscription_items
            })

        return grouped_result




    def __extract_next_event_group(self, inscriptions_pool: List[Inscription]) -> Tuple[List[Inscription], List[Inscription]]:
        """
        Extrae el siguiente grupo de inscripciones con el mismo event_id,
        basado en el primer elemento de la lista.

        :param inscriptions_pool: Lista completa de inscripciones disponibles.
        :return: Una tupla con (grupo del siguiente event_id, lista restante sin ese grupo).
        """
        if not inscriptions_pool:
            return [], []

        current_event_id = inscriptions_pool[0].event_id
        current_group = [ins for ins in inscriptions_pool if ins.event_id == current_event_id]
        updated_pool = [ins for ins in inscriptions_pool if ins.event_id != current_event_id]

        return current_group, updated_pool

    def __nameAndIdEvent(self, id_event: int):
        event = self.event_repo.find_by_id(id_event)
        return [event.id_evento, event.nombre_evento]

    def __nameAndIdArea(self, id_area: int):
        area = self.area_repo.find_by_id(id_area)
        return [area.id_area, area.nombre_area]

    def __nameAndIdCategory(self, id_category: int):
        category = self.category_repo.find_by_id(id_category)
        return [category.category_id, category.category_name]

