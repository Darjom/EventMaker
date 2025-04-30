from typing import Optional, List
from ..domain.DelegationRepository import DelegationRepository
from ..domain.Delegation import Delegation
from .persistence.DelegationMapping import DelegationMapping
from shared.extensions import db

class PostgresDelegationRepository(DelegationRepository):
    def save(self, delegation: Delegation) -> Delegation:
        delegation_mapping = DelegationMapping.from_domain(delegation)
        db.session.add(delegation_mapping)
        db.session.commit()
        return delegation_mapping.to_domain()

    def find_by_name(self, name: str) -> Optional[Delegation]:
        delegation_mapping = DelegationMapping.query.filter_by(nombre=name).first()
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