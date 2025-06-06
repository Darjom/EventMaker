from .AssignStudentToDelegation import AssignStudentToDelegation
from ..domain.DelegationRepository import DelegationRepository
from ...user.application.GetUserByEmail import GetUserByEmail
from ...user.domain.UserRepository import UserRepository
from flask_mail import Message
from shared.extensions import mail


class AssignStudentToDelegationByEmail:
    def __init__(self, repository: DelegationRepository, repository_user: UserRepository):
        self.__repository = repository
        self.__repository_user = repository_user

    def execute(self, delegation_id: int, student_email: str) -> int:
        student = GetUserByEmail(self.__repository_user).execute(student_email)

        if student is None:
            return 0  # No existe un usuario con ese correo

        if not isinstance(student.roles, list) or "student" not in student.roles:
            return 3  # El usuario no tiene rol de estudiante


        # 2. Ejecutar la asignación
        was_assigned = AssignStudentToDelegation(self.__repository).execute(
            delegation_id,
            student.id
        )

        # 3. Si se agregó exitosamente (was_assigned == True), enviar correo de notificación
        if was_assigned:
            try:
                # Obtener detalles de la delegación (por ejemplo, su nombre) para el correo.
                # Asumimos que el repository tiene un método get_by_id que retorna un objeto Delegation con atributo 'name'.
                delegation = self.__repository.find_by_id(delegation_id)

                # Construir y enviar el mensaje
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
                # Si falla el envío, registra el error en los logs (no interrumpe la ejecución)
                from flask import current_app
                current_app.logger.error(
                    f"Error al notificar por correo la asignación de estudiante {student.id} "
                    f"a delegación {delegation_id}: {e}"
                )

            return 1  # Asignado y notificación enviada

        return 2  # Ya estaba asignado (no hizo falta notificar)
