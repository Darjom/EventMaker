from modules.notifications.domain.Notification import Notification


class IEmailGateway:
    """Interfaz para el gateway de correo (Port)"""
    def send(self, notification: Notification) -> None:
        raise NotImplementedError