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

class EnviarRecordatorioCierre:
    @staticmethod
    def enviar_notificaciones_inscripcion(cls):
        """Envía notificaciones 48h antes del cierre de inscripciones"""
        tz = pytz.timezone(current_app.config['APP_TIMEZONE'])
        hoy = datetime.now(tz).date()
        fecha_objetivo = hoy + timedelta(days=2)
        
        try:
            # 1. Obtener inscripciones
            inscripciones = EnviarRecordatorioCierre._obtener_inscripciones_pendientes(fecha_objetivo)
            current_app.logger.info(f"Inscripciones a notificar: {len(inscripciones)}")
            
            # 2. Procesar envíos
            notificados = []
            for insc in inscripciones:
                usuario = insc.user
                evento = insc.event
                if EnviarRecordatorioCierre._es_usuario_valido(usuario):
                    msg = EnviarRecordatorioCierre._crear_message_cierre(usuario, evento)
                    try:
                        mail.send(msg)
                        notificados.append(insc.inscription_id)
                        # 3. Registrar en log de notificaciones
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
                            notification_type='cierre_inscripcion',
                            status='sent'
                        )
                        log.sent_at = datetime.utcnow()
                        db.session.add(log)
                    except Exception as e:
                        current_app.logger.error(f"Error enviando a {usuario.id}: {e}")
            
            # 3. Actualizar estado
            if notificados:
                EnviarRecordatorioCierre._marcar_como_notificados(notificados)
                db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.critical(f"Error en RecordatorioCierre: {str(e)}")
            raise

    @staticmethod
    def _obtener_inscripciones_pendientes(fecha):
        return (
            InscriptionMapping.query
            .join(EventMapping, InscriptionMapping.event_id == EventMapping.id_evento)
            .filter(
                db.func.date(EventMapping.fin_inscripcion) == fecha,
                InscriptionMapping.notificacion_enviada == False,
                InscriptionMapping.status.in_(["Pendiente", "En Proceso"])
            )
            .options(
                joinedload(InscriptionMapping.user),
                joinedload(InscriptionMapping.event)
            )
            .all()
        )

    @staticmethod
    def _es_usuario_valido(usuario):
        return usuario and usuario.email and getattr(usuario, 'active', False)

    @staticmethod
    def _crear_message_cierre(usuario, evento):
        return Message(
            subject=f"⏳ 48h restantes: {evento.nombre_evento}",
            recipients=[usuario.email],
            html=render_template(
                'emails/notificacion_cierre_48h.html',
                usuario=usuario,
                evento=evento,
                nombre=usuario.first_name,
                fecha_limite=evento.fin_inscripcion
            )
        )

    @staticmethod
    def _marcar_como_notificados(ids):
        InscriptionMapping.query.filter(
            InscriptionMapping.inscription_id.in_(ids)
        ).update({"notificacion_enviada": True}, synchronize_session=False)