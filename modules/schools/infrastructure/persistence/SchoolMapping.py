# modules/schools/infrastructure/persistence/SchoolMapping.py
from shared.extensions import db
from modules.schools.domain.School import School


class SchoolMapping(db.Model):
    __tablename__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def to_domain(self) -> School:
        return School(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def from_domain(cls, school: School):
        return cls(
            id=school.id,
            name=school.name
        )