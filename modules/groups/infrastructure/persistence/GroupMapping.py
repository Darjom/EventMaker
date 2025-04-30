# modules/groups/infrastructure/persistence/GruopsMapping.py
from shared.extensions import db


class DelegationMapping(db.Model):
    __tablename__ = "group"

    id_group = db.Column(db.Integer, primary_key=True)
    name_group = db.Column(db.String(100), nullable=False)

    # Relación muchos-a-uno con Evento
    id_area = db.Column(db.Integer, db.ForeignKey('area.id_area'), nullable=False)
    area = db.relationship('AreaMapping', backref=db.backref('group', lazy=True))

    def to_domain(self) -> Group:
        return Group(
            id_delegation=self.id_delegation,
            name_delegation=self.name_delegation,
            code=self.code,
            id_evento=self.id_evento
        )

    @classmethod
    def from_domain(cls, group: Group):
        return cls(
            id_delegation=delegation.id_delegation,
            name_delegation=delegation.name_delegation,
            code=delegation.code,
            id_evento=delegation.id_evento
        )
