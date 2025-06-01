from shared.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from datetime import datetime

from modules.notifications.domain.EmailAddress import EmailAddress
from modules.notifications.domain.Attachment import Attachment
from modules.notifications.domain.Notification import Notification

class NotificationMapping(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    sender_address = db.Column(db.String(255), nullable=False)
    sender_name = db.Column(db.String(255), nullable=True)
    recipient_address = db.Column(db.String(255), nullable=False)
    recipient_name = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    cc = db.Column(ARRAY(db.Text))
    bcc = db.Column(ARRAY(db.Text))
    attachments = db.Column(JSONB)  # Lista de dicts: {filename, mime_type}
    read_receipt = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    error_message = db.Column(db.Text)
    attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    sent_at = db.Column(db.DateTime(timezone=True))
    read_at = db.Column(db.DateTime(timezone=True))
    notification_type = db.Column(db.String(50), nullable=False)


    user = db.relationship("UserMapping", backref="notification")

    def to_domain(self):
        return Notification(
            sender=EmailAddress(address=self.sender_address, name=self.sender_name),
            recipient=EmailAddress(address=self.recipient_address, name=self.recipient_name),
            subject=self.subject,
            body=self.body,
            cc=[EmailAddress(address=addr) for addr in self.cc or []],
            bcc=[EmailAddress(address=addr) for addr in self.bcc or []],
            attachments=[
                Attachment(**att) for att in self.attachments or []
            ],
            read_receipt=self.read_receipt,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, domain_notification: Notification, user_id: int,notification_type: str, status="pending"):
        return cls(
            user_id=user_id,
            sender_address=domain_notification.sender.address,
            sender_name=domain_notification.sender.name,
            recipient_address=domain_notification.recipient.address,
            recipient_name=domain_notification.recipient.name,
            subject=domain_notification.subject,
            body=domain_notification.body,
            cc=[addr.address for addr in domain_notification.cc],
            bcc=[addr.address for addr in domain_notification.bcc],
            attachments=[att.__dict__ for att in domain_notification.attachments],
            read_receipt=domain_notification.read_receipt,
            status=status,
            notification_type=notification_type,
            created_at=domain_notification.created_at
        )
