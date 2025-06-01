from typing import List, Tuple

from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.Inscription import Inscription
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository



class GetStudentInscriptionsByEvent:
    def __init__(self, repository: InscriptionRepository,
                       event_repository: EventRepository,
                       area_repository: AreaRepository,
                       category_repository: CategoryRepository):
        self.__repository = repository
        self.__event_repo = event_repository
        self.__area_repo = area_repository
        self.__category_repo = category_repository

    def execute(self, event_id: int, student_id: int):
        inscriptions = self.__repository.find_by_student_and_event(student_id, event_id)
        inc, name_event = self.__group_inscriptions_by_event(inscriptions=inscriptions)
        inscriptions_dto = [InscriptionDTO.from_domain(insc) for insc in inscriptions]
        return self.transformar_areas_para_orden_pago(inc), name_event, inscriptions_dto

    def transformar_areas_para_orden_pago(self, inscriptions_event_group: list) -> list:
        areas = []

        if not inscriptions_event_group:
            return areas

        for group in inscriptions_event_group:

            if "inscriptions" not in group:
                continue  # o puedes lanzar un error si esto nunca debería pasar
            for ins in group["inscriptions"]:
                areas.append({
                    "area": ins["area_name"],
                    "categoria": ins["category_name"],
                    "monto": ins["category_monto"],
                    "status": ins["status"]
                })
        return areas

    def __group_inscriptions_by_event(self, inscriptions: List[Inscription]) -> List[dict]:
        """
        Agrupa las inscripciones por evento y devuelve una lista de diccionarios
        con la estructura deseada.
        """
        event_name =""
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
                category_id, category_name, monto = self.__nameAndIdCategory(ins.category_id)

                inscription_items.append({
                    "area_id": area_id,
                    "area_name": area_name,
                    "category_id": category_id,
                    "category_name": category_name,
                    "category_monto": monto,
                    "status": ins.status,

                })

            grouped_result.append({
                "event_id": event_id,
                "event_name": event_name,
                "inscriptions": inscription_items
            })

        return [grouped_result, event_name]


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
        event = self.__event_repo.find_by_id(id_event)
        return [event.id_evento, event.nombre_evento]

    def __nameAndIdArea(self, id_area: int):
        area = self.__area_repo.find_by_id(id_area)
        return [area.id_area, area.nombre_area]

    def __nameAndIdCategory(self, id_category: int):
        category = self.__category_repo.find_by_id(id_category)
        return [category.category_id, category.category_name, category.price]

