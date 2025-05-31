from datetime import datetime
from typing import List

from modules.notifications.domain.Attachment import Attachment
from modules.notifications.domain.EmailAddress import EmailAddress
from modules.notifications.domain.Notification import Notification
from modules.notifications.domain.NotificationRepository import NotificationRepository


class NotificationCreator:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def create(
            self,
            user_id: int,
            sender: EmailAddress,
            recipient: EmailAddress,
            subject: str,
            body: str,
            cc: List[EmailAddress] = None,
            bcc: List[EmailAddress] = None,
            attachments: List[Attachment] = None,
            read_receipt: bool = False,
            status: str = "pending"
    ) -> Notification:
        # Crear la entidad de dominio
        notification = Notification(
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            cc=cc or [],
            bcc=bcc or [],
            attachments=attachments or [],
            read_receipt=read_receipt,
            created_at=datetime.now()
        )

        # Persistir usando el repositorio
        return self.notification_repository.save(user_id, notification, status)
    