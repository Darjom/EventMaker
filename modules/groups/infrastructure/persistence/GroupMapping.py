from modules.groups.domain.Group import Group
from shared.extensions import db


tutor_grupo = db.Table(
    'tutor_grupo',
    db.Column('id_grupo', db.Integer, db.ForeignKey('grupo.id_grupo'), primary_key=True),
    db.Column('id_tutor', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class GroupMapping(db.Model):
    __tablename__ = "grupo"

    id_grupo = db.Column(db.Integer, primary_key=True)
    nombre_grupo = db.Column(db.String(100), nullable=False)

    # Relación con Área
    id_area = db.Column(db.Integer, db.ForeignKey('area.id_area'), nullable=False)
    area = db.relationship('AreaMapping', backref=db.backref('grupos', lazy=True))

    # Relación con Delegación
    id_delegacion = db.Column(db.Integer, db.ForeignKey('delegacion.id_delegacion'), nullable=False)
    delegacion = db.relationship('DelegationMapping', backref=db.backref('grupos', lazy=True))

    # Relación muchos-a-muchos con Tutores
    tutores = db.relationship(
        'UserMapping',
        secondary=tutor_grupo,
        backref=db.backref('grupos_asignados', lazy='dynamic'),
        lazy='dynamic'  # Para queries eficientes
    )

    def to_domain(self):

        return Group(
            id_grupo=self.id_grupo,
            nombre_grupo=self.nombre_grupo,
            id_area=self.id_area,
            id_delegacion=self.id_delegacion
        )

    @classmethod
    def from_domain(cls, group: Group):
        return cls(
            id_grupo=group.id_grupo,
            nombre_grupo=group.nombre_grupo,
            id_area=group.id_area,
            id_delegacion=group.id_delegacion
        )