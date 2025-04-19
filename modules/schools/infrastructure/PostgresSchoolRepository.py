# modules/schools/infrastructure/PostgresSchoolRepository.py
from typing import List, Optional
from ..domain.SchoolRepository import SchoolRepository
from ..domain.School import School
from .persistence.SchoolMapping import SchoolMapping
from shared.extensions import db

class PostgresSchoolRepository(SchoolRepository):
    def save(self, school: School) -> School:
        school_mapping = SchoolMapping.from_domain(school)
        db.session.add(school_mapping)
        db.session.commit()
        return school_mapping.to_domain()

    def find_by_id(self, school_id: int) -> Optional[School]:
        school = SchoolMapping.query.get(school_id)
        return school.to_domain() if school else None

    def find_by_name(self, name: str) -> Optional[School]:
        school = SchoolMapping.query.filter_by(name=name).first()
        return school.to_domain() if school else None

    def find_all(self) -> List[School]:
        schools = SchoolMapping.query.all()
        return [s.to_domain() for s in schools]