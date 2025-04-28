from typing import List
from ..domain.DelegationTutorRepository import DelegationTutorRepository
from ..domain.DelegationTutor import DelegationTutor
from .persistence.DelegationTutorMapping import DelegationTutorMapping
from shared.extensions import db


class PostgresDelegationTutorRepository(DelegationTutorRepository):
    def save(self, delegation_tutor: DelegationTutor) -> DelegationTutor:
        mapping = DelegationTutorMapping.from_domain(delegation_tutor)
        db.session.add(mapping)
        db.session.commit()
        return mapping.to_domain()

    def find_by_delegation(self, delegation_id: int) -> List[DelegationTutor]:
        mappings = DelegationTutorMapping.query.filter_by(delegation_id=delegation_id).all()
        return [m.to_domain() for m in mappings]

    def find_by_tutor(self, tutor_id: int) -> List[DelegationTutor]:
        mappings = DelegationTutorMapping.query.filter_by(tutor_id=tutor_id).all()
        return [m.to_domain() for m in mappings]