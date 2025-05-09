from modules.notifications.application.NotificationService import NotificationService
from modules.notifications.domain.EmailAddress import EmailAddress
from modules.notifications.domain.Notification import Notification


class AccountCreationService(NotificationService):
    """Caso de uso: Notificar creación de cuenta"""
    def _create_notification(self, user_email: EmailAddress) -> Notification:
        return Notification(
            sender = EmailAddress("no-reply@sistema.com", "Sistema de Inscripciones"),
            recipient = user_email,
            subject = "Cuenta creada exitosamente",
            body = "Su cuenta ha sido creada satisfactoriamente",
            cc=[],
            bcc=[],
            attachments=[],
            read_receipt=False
        )