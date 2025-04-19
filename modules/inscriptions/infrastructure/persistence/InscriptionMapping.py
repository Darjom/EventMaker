
from modules.inscriptions.domain.Inscription import Inscription
from shared.extensions import db


class InscriptionMapping(db.Model):
    __tablename__ = "inscription"

    # Composite primary keys and foreign keys:
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id_area'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), primary_key=True)

    # Additional fields:
    inscription_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)


    def to_domain(self):

        return Inscription(
            student_id=self.student_id,
            event_id=self.event_id,
            area_id=self.area_id,
            category_id=self.category_id,
            inscription_date=self.inscription_date,
            status=self.status
        )

    @classmethod
    def from_domain(cls, inscription):
        """
        Converts a domain Inscription object into an InscriptionMapping object.
        It is assumed that the 'inscription' object has the same attributes as defined in this model.
        """
        return cls(
            student_id=inscription.student_id,
            event_id=inscription.event_id,
            area_id=inscription.area_id,
            category_id=inscription.category_id,
            inscription_date=inscription.inscription_date,
            status=inscription.status
        )
