
from modules.schools.application.dtos.SchoolDTO import SchoolDTO
from modules.schools.application.dtos.SchoolsDTO import SchoolsDTO
from modules.schools.domain.SchoolRepository import SchoolRepository



class GetAllSchools:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repo = school_repository

    def execute(self) -> SchoolsDTO:
        schools = self.school_repo.find_all()
        school_dtos = [SchoolDTO.from_domain(school) for school in schools]
        return SchoolsDTO(schools=school_dtos)



# Para testear
if __name__ == '__main__':
    from app import app
    from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
    with app.app_context():
        school_repository = PostgresSchoolRepository()
        get_all_schools = GetAllSchools(school_repository)
        schools_dto = get_all_schools.execute()
        print(schools_dto)
