# tareas.py
from flask_mail import Message
from datetime import datetime, timedelta
from flask import render_template,current_app
from sqlalchemy.orm import joinedload
from shared.extensions import db, mail
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.inscriptions.infrastructure.persistence.InscriptionMapping import InscriptionMapping
from modules.user.infrastructure.persistence.UserMapping import UserMapping
import pytz


class EnviarRecordatorioInicio:
    @classmethod
    def enviar_notificaciones_inicio(cls):
        """Envía notificaciones 48h antes de que abran las inscripciones"""
        tz = pytz.timezone(current_app.config['APP_TIMEZONE'])
        hoy = datetime.now(tz).date()
        fecha_objetivo = hoy + timedelta(days=2)
        
        try:
            # 1. Obtener eventos
            eventos = cls._obtener_eventos_proximos(fecha_objetivo)
            current_app.logger.info(f"Eventos a notificar: {len(eventos)}")
            
            # 2. Obtener usuarios activos
            usuarios = cls._obtener_usuarios_activos()
            
            # 3. Enviar notificaciones
            for evento in eventos:
                for usuario in usuarios:
                    if usuario.email:
                        cls._enviar_email(usuario, evento)
            
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
    def _enviar_email(usuario, evento):
        try:
            msg = Message(
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
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Error enviando a {usuario.id}: {str(e)}")