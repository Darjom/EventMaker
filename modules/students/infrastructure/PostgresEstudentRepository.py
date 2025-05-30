from typing import List

from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from modules.students.domain.Student import Student
from modules.students.domain.StudentRepository import StudentRepository
from modules.students.infrastructure.persistence.StudentMapping import StudentMapping
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db

class PostgresStudentRepository(StudentRepository):

    def save(self, student: Student) -> None:
        student_mapping = StudentMapping.from_domain(student)
        db.session.add(student_mapping)
        db.session.commit()
        return student_mapping.to_domain()

    def add_roles_to_user(self, user_id: int, role_ids: List[int]) -> None:
        user_mapping = db.session.query(UserMapping).get(user_id)
        if not user_mapping:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        roles = db.session.query(RolMapping).filter(RolMapping.id.in_(role_ids)).all()
        found_ids = {role.id for role in roles}
        missing = set(role_ids) - found_ids
        if missing:
            raise ValueError(f"Roles no encontrados: {missing}")

        user_mapping.roles.extend(roles)
        db.session.commit()

    def find_by_email(self, email: str) -> Student:
        student_mapping = db.session.query(StudentMapping).filter_by(email=email).first()
        if student_mapping:
            return student_mapping.to_domain()
        return None

    def find_by_id(self, id: int) -> Student:
        student_mapping = db.session.query(StudentMapping).filter_by(id=id).first()
        if student_mapping:
            return student_mapping.to_domain()
        return None
    
    def find_by_ci(self, ci: str) -> Student:
        student_mapping = db.session.query(StudentMapping).filter_by(ci=ci).first()
        if student_mapping:
            return student_mapping.to_domain()
        return None

    def find_students_by_list_id(self, list_id: List[int]) -> list[Student]:
        students_db = db.session.query(StudentMapping).filter(StudentMapping.id.in_(list_id)).all()
        return [student.to_domain() for student in students_db]