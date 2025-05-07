from modules.notifications.domain.Notification import Notification
from modules.notifications.infrastructure.IEmailGateway import IEmailGateway


class NotificationService:
    """Servicio base para notificaciones con template method"""

    def __init__(self, email_gateway: 'IEmailGateway'):
        self.email_gateway = email_gateway

    def _create_notification(self, *args, **kwargs) -> Notification:
        """Método abstracto para implementar en subclases"""
        raise NotImplementedError

    def send(self, *args, **kwargs) -> None:
        """Template method para el flujo de envío"""
        notification = self._create_notification(*args, **kwargs)
        self.email_gateway.send(notification)
