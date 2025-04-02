from shared.extensions import db


class UserEventMapping(db.Model):
    __tablename__ = "User-Evento"

    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('Evento.id_evento'), primary_key=True)