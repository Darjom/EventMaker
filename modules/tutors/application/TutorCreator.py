from datetime import datetime

from werkzeug.security import generate_password_hash

from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.domain.TutorRepository import TutorRepository


class TutorCreator:
    def __init__(self, tutor_repository: TutorRepository):
        self.tutor_repository = tutor_repository

    def create_tutor(self, tutor_dto: TutorDTO) -> TutorDTO:

        existing_tutor = self.tutor_repository.find_by_email(tutor_dto.email)
        tutor_existente = self.tutor_repository.find_by_ci(tutor_dto.ci)
        if existing_tutor:
            raise ValueError("Tutor with this email already exists")
        elif tutor_existente:
            raise ValueError("Tutor con este CI ya existe")

        # Convertir DTO a dominio
        tutor = tutor_dto.to_domain()

        tutor.confirmed_at = datetime.now()
        tutor.password =generate_password_hash(tutor.password)
        if not tutor.roles:
            tutor.roles = [4] # id de rol tutor


        # Guardar tutor
        tutor = self.tutor_repository.save(tutor)
        self.tutor_repository.add_roles_to_user(tutor.id ,[4])

        # Retornar el DTO actualizado
        return TutorDTO.from_domain(tutor)

