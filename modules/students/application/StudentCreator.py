from datetime import datetime

from werkzeug.security import generate_password_hash

from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.domain.StudentRepository import StudentRepository


class StudentCreator:
    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    def create_student(self, student_dto: StudentDTO) -> StudentDTO:
        """
        Crea un nuevo estudiante a partir de un DTO
        """
        # Verificar si el estudiante ya existe
        existing_student = self.student_repository.find_by_email(student_dto.email)
        estudiante_existente = self.student_repository.find_by_ci(student_dto.ci)
        if existing_student:
            raise ValueError("Student with this email already exists")
        elif estudiante_existente:
            raise ValueError("Estudiante con este CI ya existe")

        # Convertir DTO a dominio
        student = student_dto.to_domain()

        student.confirmed_at = datetime.now()
        student.password =generate_password_hash(student.password)
        if not student.roles:
            student.roles = [4] # id de rol student

        school_repo=PostgresSchoolRepository()
        school= school_repo.find_by_id(student.school_id)
        if school is None:
            return None

        # Guardar el estudiante
        student = self.student_repository.save(student)
        self.student_repository.add_roles_to_user(student.id,[4])

        # Retornar el DTO actualizado
        return StudentDTO.from_domain(student)

