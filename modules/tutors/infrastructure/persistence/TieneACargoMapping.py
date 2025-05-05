
from shared.extensions import db


class TieneAcargoMapping(db.Model):
    __tablename__ = 'tieneAcargo'

    # Llave primaria compuesta
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)




