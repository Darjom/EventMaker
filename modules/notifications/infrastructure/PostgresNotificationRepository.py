from modules.notifications.domain.Notification import Notification
from modules.notifications.domain.NotificationRepository import NotificationRepository
from modules.notifications.infrastructure.persistence.NotificationMapping import NotificationMapping
from shared.extensions import db


class PostgresNotificationRepository(NotificationRepository):

    def save(self, user_id: int, notification: Notification, status: str) -> Notification:
        notification_mapping = NotificationMapping.from_domain(notification, user_id, status)
        db.session.add(notification_mapping)
        db.session.commit()
        return notification_mapping.to_domain()
