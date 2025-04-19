from app import app
from modules.tutors.application.TutorStudentAssigner import TutorStudentAssigner
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository


def test_assign_tutor_to_student():
    # Test data — asegúrate de que estos IDs existan en tu DB
    student_id = 6
    tutor_id = 3

    # Initialize the repository
    tutor_repository = PostgresTutorRepository()

    # Initialize the use case/service
    assigner = TutorStudentAssigner(tutor_repository)

    # Execute the use case
    return assigner.execute(student_id, tutor_id)


if __name__ == "__main__":
    with app.app_context():
        result = test_assign_tutor_to_student()
        print("Tutor assigned to student:" if result else "Assignment failed or already exists.")
