from datetime import date, time
from typing import Optional


class Inscription:
    """
    Constructor de la clase Inscription.

    :param student_id: Identificador del estudiante (user).
    :param event_id: Identificador del evento.
    :param area_id: Identificador del área.
    :param category_id: Identificador de la categoría.
    :param delegation_id Identificador de la delegation
    :param inscription_date: Fecha de la inscripción.
    :param status: Estado de la inscripción.
    """
    def __init__(self,
                 student_id: int,
                 event_id: int,
                 area_id: int,
                 category_id: int,
                 inscription_date: date,
                 status: str,
                 delegation_id: Optional[int] = None,
                 voucher_id: Optional[int] = None):

        self.student_id = student_id
        self.event_id = event_id
        self.area_id = area_id
        self.category_id = category_id
        self.delegation_id = delegation_id
        self.voucher_id = voucher_id
        self.inscription_date = inscription_date
        self.status = status


