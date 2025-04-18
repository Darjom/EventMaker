# test_school_creator.py
from app import app
from shared.extensions import db
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.schools.application.SchoolCreator import SchoolCreator
from modules.schools.application.dtos.SchoolDTO import SchoolDTO
from modules.user.infrastructure.persistence.UserMapping import UserMapping


def test_school_creation():
    """Test the school creation functionality"""
    with app.app_context():

     # Initialize repository and service
        school_repo = PostgresSchoolRepository()
        school_creator = SchoolCreator(school_repo)

        # Create DTO PROPERLY using keyword arguments
        school_dto = SchoolDTO(name="ExUnersity")

        # Create school

        created_school = school_creator.execute(school_dto)
        print(f"Successfully created school: {created_school}")

            # Verify the school was created
        saved_school = school_repo.find_by_id(created_school.id)
        print(f"Retrieved school from DB: {saved_school}")




if __name__ == "__main__":
    print("=== Testing School Creation ===")

    test_school_creation()
    print("=== Test Complete ===")