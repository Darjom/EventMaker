from abc import ABC, abstractmethod

from modules.notifications.domain.Notification import Notification


class NotificationRepository(ABC):

    @abstractmethod
    def save(self, user_id: int, notification: Notification, status: str) -> Notification:
        pass
