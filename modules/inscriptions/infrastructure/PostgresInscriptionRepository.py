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