from flask_mail import Message
from datetime import datetime, timedelta
from flask import render_template,current_app
from sqlalchemy.orm import joinedload
from shared.extensions import db, mail
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.inscriptions.infrastructure.persistence.InscriptionMapping import InscriptionMapping
from modules.user.infrastructure.persistence.UserMapping import UserMapping
import pytz

class EnviarRecordatorioCierre:
    @classmethod
    def enviar_notificaciones_inscripcion(cls):
        """Envía notificaciones 48h antes del cierre de inscripciones"""
        tz = pytz.timezone(current_app.config['APP_TIMEZONE'])
        hoy = datetime.now(tz).date()
        fecha_objetivo = hoy + timedelta(days=2)
        
        try:
            # 1. Obtener inscripciones
            inscripciones = cls._obtener_inscripciones_pendientes(fecha_objetivo)
            current_app.logger.info(f"Inscripciones a notificar: {len(inscripciones)}")
            
            # 2. Procesar envíos
            notificados = []
            for insc in inscripciones:
                if cls._es_usuario_valido(insc.user):
                    cls._enviar_email(insc.user, insc.event)
                    notificados.append(insc.inscription_id)
            
            # 3. Actualizar estado
            if notificados:
                cls._marcar_como_notificados(notificados)
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
    def _enviar_email(usuario, evento):
        try:
            msg = Message(
                subject=f"⏳ 48h restantes: {evento.nombre_evento}",
                recipients=[usuario.email],
                html=render_template(
                    "emails/notificacion_cierre_48h.html",
                    usuario=usuario,
                    evento=evento,
                    nombre=usuario.first_name,
                    fecha_limite=evento.fin_inscripcion
                )
            )
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Error enviando a {usuario.id}: {str(e)}")

    @staticmethod
    def _marcar_como_notificados(ids):
        InscriptionMapping.query.filter(
            InscriptionMapping.inscription_id.in_(ids)
        ).update({"notificacion_enviada": True}, synchronize_session=False)