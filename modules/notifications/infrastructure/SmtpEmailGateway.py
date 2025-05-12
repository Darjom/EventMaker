import os
import smtplib
from email.message import EmailMessage
from email.utils import formatdate

from modules.notifications.domain.Notification import Notification
from modules.notifications.infrastructure.IEmailGateway import IEmailGateway


class SmtpEmailGateway(IEmailGateway):
    """Adaptador SMTP para envío real de emails"""

    def __init__(self):
        self.server = os.getenv("SMTP_SERVER")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.user = os.getenv("SMTP_USER")
        self.password = os.getenv("SMTP_PASSWORD")

    def send(self, notification: Notification) -> None:
        msg = EmailMessage()
        self._build_headers(msg, notification)
        self._build_body(msg, notification)
        self._add_attachments(msg, notification)
        self._send(msg)

    def _build_headers(self, msg: EmailMessage, notification: Notification):
        """Construye encabezados del email"""
        msg["From"] = f"{notification.sender.name} <{notification.sender.address}>"
        msg["To"] = f"{notification.recipient.name} <{notification.recipient.address}>"
        msg["Subject"] = notification.subject
        msg["Date"] = formatdate(notification.created_at.timestamp(), localtime=True)

        if notification.cc:
            msg["Cc"] = ", ".join([f"{c.name} <{c.address}>" for c in notification.cc])

        if notification.bcc:
            msg["Bcc"] = ", ".join([f"{b.name} <{b.address}>" for b in notification.bcc])

        if notification.read_receipt:
            msg["Disposition-Notification-To"] = notification.sender.address

    def _build_body(self, msg: EmailMessage, notification: Notification):
        """Construye el cuerpo del mensaje"""
        if "<html>" in notification.body:
            msg.set_content(notification.body, subtype="html")
        else:
            msg.set_content(notification.body)

    def _add_attachments(self, msg: EmailMessage, notification: Notification):
        """Agrega archivos adjuntos"""
        for attachment in notification.attachments:
            msg.add_attachment(
                attachment.content,
                maintype=attachment.mime_type.split('/')[0],
                subtype=attachment.mime_type.split('/')[1],
                filename=attachment.filename
            )

    def _send(self, msg: EmailMessage):
        """Envía el mensaje via SMTP"""
        with smtplib.SMTP(self.server, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.send_message(msg)