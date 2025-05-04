from app import app
from modules.delegations.application.AssignStudentToDelegation import AssignStudentToDelegation
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository

def test_assign_student_to_delegation():
    # Inicializar repositorio
    delegation_repository = PostgresDelegationRepository()

    # Inicializar el servicio
    assigner = AssignStudentToDelegation(repository=delegation_repository)

    # IDs de prueba
    delegation_id = 1
    student_id = 6

    # Ejecutar la asignación
    was_assigned = assigner.execute(delegation_id, student_id)

    # Verificar el resultado
    if was_assigned:
        print(f"✅ Estudiante {student_id} fue agregado a la delegación {delegation_id}.")
    else:
        print(f"ℹ️ Estudiante {student_id} ya estaba asociado a la delegación {delegation_id}.")

if __name__ == "__main__":
    with app.app_context():
        test_assign_student_to_delegation()
