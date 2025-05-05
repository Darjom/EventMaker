from datetime import datetime

from app import app
from modules.tutors.application.FindTutorById import FindTutorById
from modules.tutors.application.UpdateTutor import UpdateTutor
from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

if __name__ == "__main__":

    with app.app_context():
        # Simulamos un tutor existente con ID 1 (deberías asegurarte que ese ID exista en la base de datos antes de correr esto)


        # Repositorio real (podrías usar un mock para test unitario si estás en entorno de pruebas)
        repository = PostgresTutorRepository()

        finder = FindTutorById(repository)
        tutorFinder = finder.execute(4)
        print("✅ Roles del tutor:", tutorFinder.roles)

        tutorFinder.email= "new.email@example.com"
        tutorFinder.first_name = "quique"
        tutorFinder.last_name = "apaza"


        # Servicio
        service = UpdateTutor(repository)

        try:
            updated_tutor_dto = service.execute(tutorFinder)
            print("✅ Tutor actualizado correctamente:")

        except Exception as e:
            print("❌ Error al actualizar tutor:", str(e))
