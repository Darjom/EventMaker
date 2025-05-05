from modules.delegations.domain.Delegation import Delegation
from shared.extensions import db



delegacion_estudiante = db.Table(
    'delegacion_estudiante',
    db.Column('id_delegacion', db.Integer, db.ForeignKey('delegacion.id_delegacion'), primary_key=True),
    db.Column('id_estudiante', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class DelegationMapping(db.Model):
    __tablename__ = "delegacion"

    id_delegacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    codigo = db.Column(db.String(50), unique=True)

    evento = db.relationship('EventMapping', backref='delegacion')

    # Relación muchos-a-muchos con Tutores
    estudiantes = db.relationship(
        'UserMapping',
        secondary=delegacion_estudiante,
        backref=db.backref('estudiantes_asignados', lazy='dynamic'),
        lazy='dynamic'  # Para queries eficientes
    )

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