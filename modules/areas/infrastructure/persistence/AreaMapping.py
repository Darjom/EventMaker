# modules/areas/infrastructure/persistence/AreaMapping.py
from shared.extensions import db
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.areas.domain.Area import Area  # Import diferido


class AreaMapping(db.Model):
    __tablename__ = "area"

    id_area = db.Column(db.Integer, primary_key=True)
    nombre_area = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(1000))
    afiche = db.Column(db.String)
    precio = db.Column(db.Integer)

    # Relación muchos-a-uno con Evento
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    evento = db.relationship('EventMapping', backref=db.backref('areas', lazy=True))

    def to_domain(self) -> Area:
        from modules.areas.domain.Area import Area  # Import diferido
        return Area(
            id_area=self.id_area,
            id_evento=self.id_evento,
            nombre_area=self.nombre_area,
            descripcion=self.descripcion,
            afiche=self.afiche,
            precio=self.precio
        )

    @classmethod
    def from_domain(cls, area: Area):
        return cls(
            id_area=area.id_area,
            id_evento=area.id_evento,
            nombre_area=area.nombre_area,
            descripcion=area.descripcion,
            afiche=area.afiche,
            precio=area.precio
        )