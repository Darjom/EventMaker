# tareas.py
from flask_mail import Message
from datetime import datetime, timedelta
from flask import render_template,current_app
from sqlalchemy.orm import joinedload
from shared.extensions import db, mail
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.inscriptions.infrastructure.persistence.InscriptionMapping import InscriptionMapping
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.notifications.infrastructure.persistence.NotificationMapping import NotificationMapping
from modules.notifications.domain.Notification import Notification as DomainNotification
from modules.notifications.domain.EmailAddress import EmailAddress
import pytz


class EnviarRecordatorioInicio:
    @staticmethod
    def enviar_notificaciones_inicio(cls):
        """Envía notificaciones 48h antes de que abran las inscripciones"""
        tz = pytz.timezone(current_app.config['APP_TIMEZONE'])
        hoy = datetime.now(tz).date()
        fecha_objetivo = hoy + timedelta(days=2)
        
        try:
            # 1. Obtener eventos
            eventos = EnviarRecordatorioInicio._obtener_eventos_proximos(fecha_objetivo)
            current_app.logger.info(f"Eventos a notificar: {len(eventos)}")
            
            # 2. Obtener usuarios activos
            usuarios = EnviarRecordatorioInicio._obtener_usuarios_activos()
            
            # 3. Enviar notificaciones
            for evento in eventos:
                for usuario in usuarios:
                    if usuario.email:
                        # 3.1 Construir el Message
                        msg = EnviarRecordatorioInicio._crear_message_inicio(usuario, evento)
                        
                        try:
                            # 3.2 Enviar correo
                            mail.send(msg)

                            # 3.3 Registrar en la tabla notification
                            domain_notif = DomainNotification(
                                sender=EmailAddress(address=current_app.config['MAIL_USERNAME'],
                                                    name=current_app.config.get('MAIL_SENDER_NAME')),
                                recipient=EmailAddress(address=usuario.email, name=usuario.first_name),
                                subject=msg.subject,
                                body=msg.html,
                                cc=[], bcc=[], attachments=[],
                                read_receipt=False,
                                created_at=datetime.utcnow()
                            )
                            log = NotificationMapping.from_domain(
                                domain_notification=domain_notif,
                                user_id=usuario.id,
                                notification_type='inicio_inscripcion',
                                status='sent'
                            )
                            log.sent_at = datetime.utcnow()
                            db.session.add(log)

                        except Exception as e:
                            current_app.logger.error(f"Error enviando recordatorio inicio a {usuario.id}: {str(e)}")

            # 4. Hacemos commit de todos los logs juntos
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            current_app.logger.critical(f"Error en RecordatorioInicio: {str(e)}")
            raise

    @staticmethod
    def _obtener_eventos_proximos(fecha):
        return EventMapping.query.filter(
            db.func.date(EventMapping.inicio_inscripcion) == fecha
        ).all()

    @staticmethod
    def _obtener_usuarios_activos():
        return UserMapping.query.filter_by(active=True).all()

    @staticmethod
    def _crear_message_inicio(usuario, evento):
        """
        Construye y devuelve el objeto Message para notificar el inicio de inscripciones.
        """
        return Message(
            subject=f"📢 ¡Inscripciones en 48h para: {evento.nombre_evento}!",
            recipients=[usuario.email],
            html=render_template(
                "emails/notificacion_inicio_48h.html",
                usuario=usuario,
                evento=evento,
                nombre=usuario.first_name,
                fecha_inicio=evento.inicio_inscripcion
            )
        )