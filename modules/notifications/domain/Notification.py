from datetime import datetime
from typing import List

from modules.notifications.domain.Attachment import Attachment
from modules.notifications.domain.EmailAddress import EmailAddress


@dataclass
class Notification:
    """Entidad principal para representar una notificación"""
    sender: EmailAddress
    recipient: EmailAddress
    subject: str
    body: str
    cc: List[EmailAddress]
    bcc: List[EmailAddress]
    attachments: List[Attachment]
    read_receipt: bool
    created_at: datetime = datetime.now()