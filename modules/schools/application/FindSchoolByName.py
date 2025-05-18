from typing import Optional
from modules.schools.application.dtos.SchoolDTO import SchoolDTO
from modules.schools.domain.SchoolRepository import SchoolRepository


class FindSchoolByName:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repo = school_repository

    def execute(self, school_name: str) -> Optional[SchoolDTO]:
        """
        Convierte una entidad School a SchoolDTO usando el método from_domain.
        """
        school = self.school_repo.find_by_name(school_name)
        if school is None:
            return None
        return SchoolDTO.from_domain(school)
