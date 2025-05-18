from modules.schools.application.dtos.SchoolDTO import SchoolDTO
from modules.schools.domain.SchoolRepository import SchoolRepository


class FindSchoolById:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repo = school_repository

    def execute(self, school_id: int) -> SchoolDTO:
        """
        Convierte una entidad School a SchoolDTO usando el método from_domain.
        """
        school = self.school_repo.find_by_id(school_id)
        if school is None:
            raise ValueError(f"Escuela con ID {school_id} no encontrada")
        return SchoolDTO.from_domain(school)
