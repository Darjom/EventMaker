from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db
from modules.events.domain.Event import Event  # Importar la clase Event del dominio


users_events = db.Table(
    'user_events',
    db.Column('id_evento', db.Integer, db.ForeignKey('evento.id_evento'), primary_key=True),
    db.Column('id_user', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class EventMapping(db.Model):
    __tablename__ = "evento"

    id_evento = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.String(150))
    tipo_evento = db.Column(db.String(50))
    descripcion_evento = db.Column(db.String(1000))
    inicio_evento = db.Column(db.DateTime)
    fin_evento = db.Column(db.DateTime)
    capacidad_evento = db.Column(db.Integer)
    inscripcion = db.Column(db.String(100))
    requisitos = db.Column(db.String())
    ubicacion = db.Column(db.String(250))
    slogan = db.Column(db.String(500))
    afiche = db.Column(db.String)

    # Relación muchos a muchos
    users = db.relationship(
        'UserMapping',
        secondary=users_events,
        backref=db.backref('created_events', lazy='dynamic')  # 🔹 Lazy loading para eficiencia
    )

    def to_domain(self) -> Event:
        """Convierte un objeto EventMapping en un objeto de dominio Event."""
        return Event(
            id_evento=self.id_evento,
            nombre_evento=self.nombre_evento,
            tipo_evento=self.tipo_evento,
            descripcion_evento=self.descripcion_evento,
            inicio_evento=self.inicio_evento,
            fin_evento=self.fin_evento,
            capacidad_evento=self.capacidad_evento,
            inscripcion=self.inscripcion,
            requisitos=self.requisitos,
            ubicacion=self.ubicacion,
            slogan=self.slogan,
            afiche=self.afiche,
            creador_id=[user.id for user in self.users]
        )

    @classmethod
    def from_domain(cls, event: Event):
        """Convierte un objeto de dominio Event en un objeto EventMapping listo para la base de datos."""
        return cls(
            id_evento=event.id_evento,  # Si id_evento es None, SQLAlchemy lo generará automáticamente
            nombre_evento=event.nombre_evento,
            tipo_evento=event.tipo_evento,
            descripcion_evento=event.descripcion_evento,
            inicio_evento=event.inicio_evento,
            fin_evento=event.fin_evento,
            capacidad_evento=event.capacidad_evento,
            inscripcion=event.inscripcion,
            requisitos=event.requisitos,
            ubicacion=event.ubicacion,
            slogan=event.slogan,
            afiche=event.afiche,
        )
