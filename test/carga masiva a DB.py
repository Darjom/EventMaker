import os

from modules.delegations.application.BulkStudentDelegationAdder import BulkStudentDelegationAdder
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.schools.application.FindSchoolByName import FindSchoolByName
from modules.schools.application.SchoolCreator import SchoolCreator
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository

from modules.user.application.GetUserByEmail import GetUserByEmail
from modules.students.application.GetStudentByCI import GetStudentByCI
from modules.students.application.StudentCreator import StudentCreator
from modules.delegations.application.AssignStudentToDelegation import AssignStudentToDelegation
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository


def test_bulk_add_students_to_delegation_real(excel_file_path: str, delegacion_id: int = 1):
    """
    Prueba real (sin mocks) del agregado masivo de estudiantes a una delegación desde un archivo Excel.
    Requiere base de datos conectada y configurada.
    """
    if not os.path.exists(excel_file_path):
        print(f"❌ Archivo no encontrado: {excel_file_path}")
        return

    try:
        # Instanciar los repositorios reales
        school_repo = PostgresSchoolRepository()
        user_repo = PostgresUserRepository()
        student_repo = PostgresStudentRepository()
        delegation_repo = PostgresDelegationRepository()

        # Casos de uso reales con inyección de dependencias
        school_finder = FindSchoolByName(school_repo)
        school_creator = SchoolCreator(school_repo)
        user_email_checker = GetUserByEmail(user_repo)
        student_ci_checker = GetStudentByCI(student_repo)
        student_creator = StudentCreator(student_repo)
        add_delegation = AssignStudentToDelegation(delegation_repo)

        # Servicio principal
        bulk_adder = BulkStudentDelegationAdder(
            school_finder,
            school_creator,
            user_email_checker,
            student_ci_checker,
            student_creator,
            add_delegation
        )

        # Ejecutar el proceso con el archivo real
        with open(excel_file_path, "rb") as f:
            observaciones = bulk_adder.execute(f, delegacion_id)

        print("✅ Proceso completado.")
        if observaciones:
            print(f"\n⚠️ Observaciones ({len(observaciones)}):")
            for obs in observaciones:
                print(f"- {obs['observacion']}: {obs['motivo']}")
        else:
            print("✅ Todos los estudiantes fueron agregados sin observaciones.")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    ruta_excel = "/Users/jose/Documents/Pycharm/EventMaker/test/Registrar estudiantes-2.xlsx"
    test_bulk_add_students_to_delegation_real(ruta_excel)
