from typing import Optional, List
from ..domain.Inscription import Inscription
from .persistence.InscriptionMapping import InscriptionMapping
from shared.extensions import db
from ..domain.InscriptionsRepository import InscriptionRepository


class PostgresInscriptionRepository(InscriptionRepository):
    def save(self, inscription: Inscription) -> Inscription:
        inscription_mapping = InscriptionMapping.from_domain(inscription)
        db.session.add(inscription_mapping)
        db.session.commit()
        return inscription_mapping.to_domain()

    def find_by_ids(self, student_id, event_id, area_id, category_id) -> Optional[Inscription]:
        inscription = InscriptionMapping.query.filter_by(
            student_id=student_id,
            event_id=event_id,
            area_id=area_id,
            category_id=category_id
        ).first()
        return inscription.to_domain() if inscription else None

    def find_by_id_student(self, student_id: int) -> List[Inscription]:
        inscriptions = InscriptionMapping.query.filter_by(student_id=student_id).all()
        return [inscription.to_domain() for inscription in inscriptions]

    def find_by_student_and_event(self, student_id: int, event_id: int) -> List[Inscription]:
        inscriptions = InscriptionMapping.query.filter_by(
            student_id=student_id,
            event_id=event_id
        ).all()
        return [inscription.to_domain() for inscription in inscriptions]

    def find_by_delegation_id(self, delegation_id: int) -> List[Inscription]:
        inscriptions = InscriptionMapping.query.filter_by(delegation_id=delegation_id).all()
        return [inscription.to_domain() for inscription in inscriptions]

    def update_all(self, inscriptions: List[Inscription]) -> List[Inscription]:
        for insc in inscriptions:
            existing = InscriptionMapping.query.filter_by(
                student_id=insc.student_id,
                event_id=insc.event_id,
                area_id=insc.area_id,
                category_id=insc.category_id
            ).first()

            if existing:
                existing.status = insc.status
                existing.voucher_id = insc.voucher_id

        db.session.commit()

        return inscriptions

    def update(self, inscription: Inscription) -> Inscription:
        # Buscar la inscripción existente en la base de datos por ID
        existing = InscriptionMapping.query.filter_by(inscription_id=inscription.inscription_id).first()

        if not existing:
            raise ValueError("Inscription not found")

        # Actualizar los campos editables
        existing.area_id = inscription.area_id
        existing.category_id = inscription.category_id
        existing.voucher_id = inscription.voucher_id if inscription.voucher_id else None
        existing.status = inscription.status

        # Guardar cambios en la base de datos
        db.session.commit()

        # Retornar la inscripción actualizada
        return existing.to_domain()

    def find_by_id(self, inscription_id: int) -> Optional[Inscription]:
        inscription = InscriptionMapping.query.filter_by(inscription_id=inscription_id).first()
        return inscription.to_domain() if inscription else None

    def delete(self, inscription: Inscription) -> None:
        inscription_mapping = InscriptionMapping.query.filter_by(
            inscription_id=inscription.inscription_id
        ).first()

        if inscription_mapping:
            db.session.delete(inscription_mapping)
            db.session.commit()

    def find_by_id_event(self, event_id: int) -> Optional[List[Inscription]]:
        inscription = InscriptionMapping.query.filter_by(event_id=event_id).first()
        return inscription.to_domain() if inscription else None
