# modules/delegations/infrastructure/persistence/DelegationMapping.py

from modules.delegations.domain.DelegationTutor import DelegationTutor  # Asegúrate de tener este domain
from shared.extensions import db

class DelegationTutorMapping(db.Model):
    __tablename__ = "delegation_tutor"

    # Claves primarias compuestas y claves foráneas:
    delegation_id = db.Column(db.Integer, db.ForeignKey('delegacion.id_delegacion'), primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

    # Métodos de conversión:

    def to_domain(self):
        return DelegationTutor(
            delegation_id=self.delegation_id,
            tutor_id=self.tutor_id,
            role_id=self.role_id
        )

    @classmethod
    def from_domain(cls, delegation_tutor):
        """
        Convierte un objeto de dominio DelegationTutor a un DelegationTutorMapping.
        Se asume que el objeto 'delegation_tutor' tiene los mismos atributos que el modelo.
        """
        return cls(
            delegation_id=delegation_tutor.delegation_id,
            tutor_id=delegation_tutor.tutor_id,
            role_id=delegation_tutor.role_id
        )
