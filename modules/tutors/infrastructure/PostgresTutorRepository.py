from typing import List

from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from modules.tutors.domain.Tutor import Tutor
from modules.tutors.domain.TutorRepository import TutorRepository
from modules.tutors.infrastructure.persistence.TieneACargoMapping import TieneAcargoMapping
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db

class PostgresTutorRepository(TutorRepository):

    def save(self, tutor: Tutor) -> None:
        tutor_mapping = UserMapping.from_domain(tutor)
        db.session.add(tutor_mapping)
        db.session.commit()
        return tutor_mapping.to_domain()

    def add_roles_to_user(self, tutor_id: int, role_ids: List[int]) -> None:
        print("user ", tutor_id)
        tutor_mapping = db.session.query(UserMapping).get(tutor_id)
        if not tutor_mapping:
            raise ValueError(f"Usuario con ID {tutor_id} no encontrado")

        roles = db.session.query(RolMapping).filter(RolMapping.id.in_(role_ids)).all()
        found_ids = {role.id for role in roles}
        missing = set(role_ids) - found_ids
        if missing:
            raise ValueError(f"Roles no encontrados: {missing}")

        tutor_mapping.roles.extend(roles)
        db.session.commit()

    def find_by_email(self, email: str):
        tutor_mapping = db.session.query(UserMapping).filter_by(email=email).first()
        if tutor_mapping:
            return tutor_mapping.to_domain()
        return None

    def find_by_id(self, id: int):
        tutor_mapping = db.session.query(UserMapping).filter_by(id=id).first()
        print("✅ Roles del tutor:", tutor_mapping.roles[0].id)
        if tutor_mapping:
            return tutor_mapping.to_domain()
        return None

    def assign_tutorship(self, student_id: int, tutor_id: int):

        existing_relationship = TieneAcargoMapping.query.filter_by(student_id=student_id, tutor_id=tutor_id).first()
        if existing_relationship:
            print("The relationship already exists.")
            return False

        # Create the new relationship
        new_relationship = TieneAcargoMapping(student_id=student_id, tutor_id=tutor_id)
        db.session.add(new_relationship)
        db.session.commit()
        print("Relationship successfully added.")
        return True

    def update(self, tutor: Tutor) -> Tutor:
        tutor_mapping = db.session.query(UserMapping).filter_by(id=tutor.id).first()
        if not tutor_mapping:
            raise ValueError("Tutor not found")

        # Actualizar los campos manualmente
        tutor_mapping.first_name = tutor.first_name
        tutor_mapping.last_name = tutor.last_name
        tutor_mapping.email = tutor.email
        tutor_mapping.password = tutor.password
        tutor_mapping.active = tutor.active
        tutor_mapping.confirmed_at = tutor.confirmed_at
        tutor_mapping.fs_uniquifier = tutor.fs_uniquifier
        tutor_mapping.ci = tutor.ci
        tutor_mapping.expedito_ci = tutor.expedito_ci
        tutor_mapping.fecha_nacimiento = tutor.fecha_nacimiento

        db.session.commit()
        return tutor_mapping.to_domain()

    def find_students(self, tutor_id: int) -> List[int]:
        students = db.session.query(TieneAcargoMapping).filter_by(tutor_id=tutor_id).all()
        students_ids = []
        for student in students:
            students_ids.append(student.student_id)
        return students_ids