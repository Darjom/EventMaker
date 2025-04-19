from datetime import datetime

from app import app
from modules.tutors.application.UpdateTutor import UpdateTutor
from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

if __name__ == "__main__":

    with app.app_context():
        # Simulamos un tutor existente con ID 1 (deberías asegurarte que ese ID exista en la base de datos antes de correr esto)
        tutor_dto = TutorDTO(
            id=4,
            first_name="José Actualizado",
            last_name="Apellido Nuevo",
            email="nuevo.email@example.com",
            password="nueva_clave_segura",
            ci="12345678",
            expedito_ci="CB",
            fecha_nacimiento=datetime(1990, 1, 1),

        )

        # Repositorio real (podrías usar un mock para test unitario si estás en entorno de pruebas)
        repository = PostgresTutorRepository()

        # Servicio
        service = UpdateTutor(repository)

        try:
            updated_tutor_dto = service.execute(tutor_dto)
            print("✅ Tutor actualizado correctamente:")
            print(tutor_dto.id, tutor_dto.first_name)
        except Exception as e:
            print("❌ Error al actualizar tutor:", str(e))
