from modules.delegations.domain.Delegation import Delegation
from shared.extensions import db



class DelegationMapping(db.Model):
    __tablename__ = "delegacion"

    id_delegacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    codigo = db.Column(db.String(50), unique=True)

    evento = db.relationship('EventMapping', backref='delegacion')

    def to_domain(self):
        return Delegation(
            id_delegacion=self.id_delegacion,
            nombre=self.nombre,
            evento_id=self.evento_id,
            codigo=self.codigo
        )

    @classmethod
    def from_domain(cls, delegation):
        return cls(
            nombre=delegation.nombre,
            evento_id=delegation.evento_id,
            codigo=delegation.codigo
        )