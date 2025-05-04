from typing import Optional, List

from .persistence.DelegationTutorMapping import DelegationTutorMapping
from ..domain.DelegationRepository import DelegationRepository
from ..domain.Delegation import Delegation
from .persistence.DelegationMapping import DelegationMapping, delegacion_estudiante
from shared.extensions import db
from ...user.infrastructure.persistence.UserMapping import UserMapping


class PostgresDelegationRepository(DelegationRepository):
    def save(self, delegation: Delegation) -> Delegation:
        delegation_mapping = DelegationMapping.from_domain(delegation)
        db.session.add(delegation_mapping)
        db.session.commit()
        return delegation_mapping.to_domain()

    def find_by_name(self, name: str) -> Optional[Delegation]:
        delegation_mapping = DelegationMapping.query.filter_by(nombre=name).first()
        return delegation_mapping.to_domain() if delegation_mapping else None

    def find_by_delegation_id(self, delgation_id: int) -> Optional[Delegation]:
        delegation_mapping = DelegationMapping.query.filter_by( id_delegacion=delgation_id).first()
        return delegation_mapping.to_domain() if delegation_mapping else None

    def find_by_event_id(self, event_id: int) -> List[Delegation]:
        delegations = DelegationMapping.query.filter_by(evento_id=event_id).all()
        return [d.to_domain() for d in delegations]

    def find_by_code(self, code: str) -> Optional[Delegation]:
        delegation_mapping = DelegationMapping.query.filter_by(codigo=code).first()
        return delegation_mapping.to_domain() if delegation_mapping else None

    def find_by_ids(self, delegation_ids: List[int]) -> List[Delegation]:
        delegations = DelegationMapping.query.filter(
            DelegationMapping.id_delegacion.in_(delegation_ids)
        ).all()
        return [d.to_domain() for d in delegations]

    def assign_student_to_delegation(self, delegation_id: int, student_id: int) -> bool:
        delegation = DelegationMapping.query.filter_by(id_delegacion=delegation_id).first()
        if not delegation:
            raise ValueError(f"Delegation with ID {delegation_id} not found.")


        student = UserMapping.query.filter_by(id=student_id).first()
        if not student:
            raise ValueError(f"Student with ID {student_id} not found.")

        if student in delegation.estudiantes:
            return False  # Ya está asociado

        delegation.estudiantes.append(student)
        db.session.commit()
        return True  # Se agregó exitosamente

    def get_student_ids_by_delegation_id(self, delegation_id: int) -> list[int]:
        result = db.session.execute(
            db.select(delegacion_estudiante.c.id_estudiante).where(
                delegacion_estudiante.c.id_delegacion == delegation_id
            )
        )
        return [row[0] for row in result]

    def get_tutor_ids_by_delegation_id(self, delegation_id: int) -> list[int]:
        result = (
            db.session.query(DelegationTutorMapping.tutor_id)
            .filter_by(delegation_id=delegation_id)
            .distinct()
            .all()
        )
        return [row[0] for row in result]