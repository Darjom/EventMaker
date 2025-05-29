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
                 notificacion_enviada: bool = False,
                 delegation_id: Optional[int] = None,
                 inscription_id: Optional[int] = None,
                 voucher_id: Optional[int] = None):

        self.inscription_id = inscription_id
        self.student_id = student_id
        self.event_id = event_id
        self.area_id = area_id
        self.category_id = category_id
        self.delegation_id = delegation_id
        self.voucher_id = voucher_id
        self.inscription_date = inscription_date
        self.status = status
        self.notificacion_enviada = notificacion_enviada

    def is_confirmed(self) -> bool:
        if self.status == "Confirmado":
            return True
        else:
            return False

    def remove_voucher(self):
        self.voucher_id = None

    def update_status(self):
        self.status = "Pendiente"

    ALLOWED_TRANSITIONS = {
    "Pendiente": ["En Proceso"],
    "En Proceso": ["Confirmado"],
    "Confirmado": []  # Estado final
    }

    def change_status(self, nuevo_estado: str):
        if nuevo_estado not in self.ALLOWED_TRANSITIONS.get(self.status, []):
            raise ValueError(f"Transición no permitida: {self.status} → {nuevo_estado}")
        self.status = nuevo_estado