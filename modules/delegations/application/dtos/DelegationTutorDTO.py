from pydantic import BaseModel

from modules.delegations.domain.DelegationTutor import DelegationTutor


class DelegationTutorDTO(BaseModel):
    delegation_id: int
    tutor_id: int
    role_id: int

    @classmethod
    def from_domain(cls, delegation_tutor):
        return cls(
            delegation_id=delegation_tutor.delegation_id,
            tutor_id=delegation_tutor.tutor_id,
            role_id=delegation_tutor.role_id
        )

    def to_domain(self):
        return DelegationTutor(
            delegation_id=self.delegation_id,
            tutor_id=self.tutor_id,
            role_id=self.role_id
        )