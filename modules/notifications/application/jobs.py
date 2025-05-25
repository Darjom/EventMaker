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

def enviar_notificaciones_inscripcion(app):
    with app.app_context():
            try:
                tz = pytz.timezone(app.config['APP_TIMEZONE'])
                hoy = datetime.now(tz).date()
                fecha_obj = hoy + timedelta(days=2)

                inscripciones = (
                    db.session.query(InscriptionMapping)
                    .join(EventMapping, InscriptionMapping.event_id == EventMapping.id_evento)
                    .filter(
                        db.func.date(EventMapping.fin_inscripcion) == fecha_obj,
                        InscriptionMapping.notificacion_enviada == False,
                        InscriptionMapping.status.in_(["Pendiente", "En Proceso"])
                    )
                    .options(
                        joinedload(InscriptionMapping.user),
                        joinedload(InscriptionMapping.event)
                    )
                    .all()
                )

                print("Total inscripciones encontradas:", len(inscripciones))
                notificados = []

                for insc in inscripciones:
                    usuario = insc.user
                    evento = insc.event

                    if not (usuario and usuario.email and evento and getattr(usuario, 'active', False)):
                        continue

                    try:
                        with app.test_request_context():
                            msg = Message(
                                subject=f"⏳ 48h restantes: {evento.nombre_evento}",
                                recipients=[usuario.email],
                                html=render_template(
                                    "emails/notificacion_48h.html",
                                    usuario=usuario,
                                    evento=evento,
                                    nombre=usuario.first_name,
                                    fecha_limite=evento.fin_inscripcion
                                )
                        )
                        mail.send(msg)
                        notificados.append(insc.inscription_id)
                    except Exception as e:
                        app.logger.error(f"Error enviando a {usuario.id}: {e}")

                if notificados:
                    db.session.query(InscriptionMapping) \
                        .filter(InscriptionMapping.inscription_id.in_(notificados)) \
                        .update({"notificacion_enviada": True}, synchronize_session=False)
                    db.session.commit()

            except Exception as e:
                db.session.rollback()
                app.logger.critical(f"Fallo general en notificaciones: {e}")
                raise

def enviar_notificaciones_inicio(app):
    with app.app_context():
        try:
            tz = pytz.timezone(current_app.config['APP_TIMEZONE'])
            hoy = datetime.now(tz).date()
            fecha_objetivo = hoy + timedelta(days=2)

            eventos = (
                db.session.query(EventMapping)
                .filter(
                    db.func.date(EventMapping.inicio_inscripcion) == fecha_objetivo
                )
                .all()
            )
            print("Total eventos encontrados con inscripciones en 48h:", len(eventos))
            for evento in eventos:
                usuarios_activos = (
                    db.session.query(UserMapping)
                    .filter(UserMapping.active == True)
                    .all()
                )

                for usuario in usuarios_activos:
                    if not usuario.email:
                        continue

                    try:
                        with app.test_request_context():
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
                        current_app.logger.error(f"Error enviando a {usuario.id}: {e}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.critical(f"Fallo general en notificaciones de inicio: {e}")
            raise