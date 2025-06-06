from ..domain.DelegationRepository import DelegationRepository
# Importaciones para notificación
from flask_mail import Message
from shared.extensions import mail
from flask import current_app

class AssignStudentToDelegation:
    def __init__(self, delegation_repo: DelegationRepository, user_repo):
        self.delegation_repo = delegation_repo
        self.user_repo = user_repo
    def execute(self, delegation_id: int, student_id: int) -> bool:
        """
        Assigns a student to a delegation.

        Returns:
            True if the student was newly associated.
            False if the student was already associated.
        """
        was_assigned = self.delegation_repo.assign_student_to_delegation(
            delegation_id,
            student_id
        )

        # 2. Si era una nueva asociación, enviamos la notificación
        if was_assigned:
            try:
                # 2.1 Obtener detalles del estudiante
                student = self.user_repo.find_by_id(student_id)
                # 2.2 Obtener detalles de la delegación
                delegation = self.delegation_repo.find_by_id(delegation_id)

                if student and delegation:
                    # Construir el mensaje y enviarlo
                    msg = Message(
                        subject="🎉 Has sido asignado a una delegación",
                        recipients=[student.email],
                        html=f"""
                            <p>Hola {student.first_name},</p>
                            <p>Has sido añadido a la delegación <strong>{delegation.name}</strong>.</p>
                            <p>¡Éxitos en tu participación!</p>
                        """
                    )
                    mail.send(msg)

            except Exception as e:
                # Logueamos el error, pero no fallamos la asignación
                current_app.logger.error(
                    f"Error al notificar por correo la asignación de estudiante {student_id} "
                    f"a delegación {delegation_id}: {e}"
                )

        return was_assigned
