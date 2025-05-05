from typing import List, Tuple, Dict

from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.Inscription import Inscription
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.domain.StudentRepository import StudentRepository


class GetStudentInscriptionsByDelegation:
    def __init__(self, repository: InscriptionRepository,
                 student_repository: StudentRepository,
                 event_repository: EventRepository,
                 area_repository: AreaRepository,
                 category_repository: CategoryRepository):
        self.__repository = repository
        self.__student_repository = student_repository
        self.__event_repo = event_repository
        self.__area_repo = area_repository
        self.__category_repo = category_repository

    def execute(self, delegation_id: int):
        """
        Obtiene las inscripciones de los estudiantes por delegación, agrupadas por estudiante.
        Devuelve un diccionario con la información del estudiante, su curso y sus inscripciones
        (áreas, categorías y precios).
        """
        # Obtener inscripciones de la delegación
        inscriptions_delegation = self.__repository.find_by_delegation_id(delegation_id)
        if len(inscriptions_delegation) == 0:
            return None
        inscriptions_dto = [InscriptionDTO.from_domain(insc) for insc in inscriptions_delegation]
        event_name = self.__nameAndIdEvent(inscriptions_delegation[0].event_id)

        # Agrupar las inscripciones por estudiante
        students_info = self.__group_inscriptions_by_student(inscriptions_delegation)

        return students_info, event_name, inscriptions_dto

    def __group_inscriptions_by_student(self, inscriptions: List[Inscription]) -> Dict:
        """
        Agrupa las inscripciones por estudiante y devuelve un diccionario con la estructura deseada.
        """
        students_info = {}

        for ins in inscriptions:
            # Obtener datos del estudiante
            student = self.__student_repository.find_by_id(ins.student_id)
            student_name = f"{student.first_name} {student.last_name}"

            # Si el estudiante no está en el diccionario, inicializamos su información
            if student_name not in students_info:
                students_info[student_name] = {
                    "curso": student.course,  # Su curso
                    "inscripciones": []  # Las inscripciones de este estudiante
                }

            # Obtener información de la inscripción
            area_id, area_name = self.__nameAndIdArea(ins.area_id)
            category_id, category_name, monto = self.__nameAndIdCategory(ins.category_id)

            # Agregar la inscripción al estudiante correspondiente
            students_info[student_name]["inscripciones"].append({
                "area_name": area_name,
                "category_name": category_name,
                "category_monto": monto,
            })

        return students_info

    def __nameAndIdEvent(self, id_event: int):
        event = self.__event_repo.find_by_id(id_event)
        return event.nombre_evento

    def __nameAndIdArea(self, id_area: int):
        """
        Devuelve el nombre del área y su ID correspondiente.
        """
        area = self.__area_repo.find_by_id(id_area)
        return area.id_area, area.nombre_area

    def __nameAndIdCategory(self, id_category: int):
        """
        Devuelve el nombre de la categoría y su monto correspondiente.
        """
        category = self.__category_repo.find_by_id(id_category)
        return category.category_id, category.category_name, category.price
