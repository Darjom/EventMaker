from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, make_response
from datetime import datetime

from flask_mail import Message
from shared.extensions import mail, db

from modules.tutors.application.TutorCreator import TutorCreator
from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

from modules.tutors.application.TutorStudentAssigner import TutorStudentAssigner
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository

from modules.notifications.infrastructure.persistence.NotificationMapping import NotificationMapping
from modules.notifications.domain.Notification import Notification as DomainNotification
from modules.notifications.domain.EmailAddress import EmailAddress

tutores_bp = Blueprint("tutores_bp", __name__)

@tutores_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        form = request.form

        # 1) Validación de contraseñas
        if form.get("password") != form.get("confirm_password"):
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("tutors/registro.html")

        email = form.get("email")

        try:
            # 2) Crear el tutor en la base de datos (commit interno). 
            #    Si falla aquí, cae en el except siguiente.
            tutor_dto = TutorDTO(
                first_name=form.get("first_name"),
                last_name=form.get("last_name"),
                email=email,
                password=form.get("password"),
                ci=form.get("ci"),
                expedito_ci=form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(form.get("fecha_nacimiento"), "%Y-%m-%d")
            )
            creado = TutorCreator(PostgresTutorRepository()).create_tutor(tutor_dto)
            # → 'creado' es el objeto dominio/postgresql con el id ya asignado.

            # 3) Enviar el correo de bienvenida SOLO SI la creación fue exitosa
            msg = Message(
                subject="¡Bienvenido como Tutor a EventMaker UMSS!",
                recipients=[email],
                html=render_template(
                    "emails/confirmacion_registro.html",
                    nombre=form.get("first_name"),
                    email=email,
                    rol="Tutor"
                ),
                charset="utf-8"
            )
            mail.send(msg)

            # 4) Registrar la notificación en la tabla `notification`
            domain_notif = DomainNotification(
                sender=EmailAddress(
                    address=current_app.config['MAIL_USERNAME'],
                    name=current_app.config.get('MAIL_SENDER_NAME')
                ),
                recipient=EmailAddress(
                    address=creado.email,
                    name=creado.first_name
                ),
                subject=msg.subject,
                body=msg.html,
                cc=[],
                bcc=[],
                attachments=[],
                read_receipt=False,
                created_at=datetime.utcnow()
            )
            log = NotificationMapping.from_domain(
                domain_notification=domain_notif,
                user_id=creado.id,
                notification_type='confirmacion_registro_tutor',
                status='sent'
            )
            log.sent_at = datetime.utcnow()
            db.session.add(log)
            db.session.commit()

            flash("✓ Cuenta de tutor creada exitosamente. Por favor revisa tu correo para confirmación.", "success")
            return redirect(url_for("admin_bp.login"))

        except Exception as e:
            # Si falla la creación o el envío del correo, revertimos todo
            db.session.rollback()
            flash(f"Error al crear cuenta de tutor o enviar correo: {e}", "danger")

            # Intentamos eliminar cualquier usuario huérfano (si es que se creó)
            posible_user = PostgresTutorRepository().find_by_email(email)
            if posible_user:
                db.session.delete(posible_user)
                db.session.commit()

            return render_template("tutors/registro.html")

    # GET → Mostrar formulario sin cache
    response = make_response(render_template("tutors/registro.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@tutores_bp.route("/agregar-estudiante", methods=["POST"])
def agregar_estudiante():
    tutor_id = session.get("admin_user")
    if not tutor_id:
        flash("Debes iniciar sesión como tutor.", "danger")
        return redirect(url_for("admin_bp.login"))

    student_email = request.form.get("student_email")
    if not student_email:
        flash("El correo electrónico es obligatorio.", "danger")
        return redirect(url_for("tutores_bp.dashboard"))

    student = PostgresStudentRepository().find_by_email(student_email)
    if not student:
        flash("No se encontró un estudiante con ese correo electrónico.", "danger")
        return redirect(url_for("tutores_bp.dashboard"))

    try:
        TutorStudentAssigner(PostgresTutorRepository()).execute(
            student_id=student.id,
            tutor_id=tutor_id
        )
        flash("Estudiante agregado exitosamente.", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("tutores_bp.dashboard"))
