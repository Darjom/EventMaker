from datetime import datetime
from typing import List

from modules.notifications.application.NotificationService import NotificationService
from modules.notifications.domain.Attachment import Attachment
from modules.notifications.domain.EmailAddress import EmailAddress
from modules.notifications.domain.Notification import Notification


class DeadlineReminderService(NotificationService):
    """Caso de uso: Recordatorio de plazo próximo a vencer"""

    def _create_notification(self,
                             user_email: EmailAddress,
                             deadline: datetime,
                             attachments: List[str] = []) -> Notification:
        return Notification(
            sender=EmailAddress("recordatorios@sistema.com", "Sistema de Recordatorios"),
            recipient=user_email,
            subject=f"Recordatorio: Plazo vence {deadline.strftime('%d/%m')}",
            body=f"""Estimado usuario,

            Le recordamos que el plazo de inscripción finaliza el {deadline.strftime('%d/%m/%Y a las %H:%M')}.

            Atentamente,
            Equipo de Inscripciones""",
            cc=[],
            bcc=[EmailAddress("auditoria@sistema.com")],
            attachments=[Attachment.from_file(f) for f in attachments],
            read_receipt=True
        )