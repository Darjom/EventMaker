from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from datetime import datetime
from flask_mail import Message
from shared.extensions import mail, db
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.application.StudentCreator import StudentCreator
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.schools.application.GetAllSchools import GetAllSchools
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.schools.application.SchoolCreator import SchoolCreator
from modules.schools.application.dtos.SchoolDTO import SchoolDTO
from modules.notifications.infrastructure.persistence.NotificationMapping import NotificationMapping
from modules.notifications.domain.Notification import Notification as DomainNotification
from modules.notifications.domain.EmailAddress import EmailAddress
import smtplib

estudiantes_bp = Blueprint("estudiantes_bp", __name__, template_folder="templates")

@estudiantes_bp.route("/registro", methods=["GET", "POST"])
def registro():
    school_repo = PostgresSchoolRepository()

    if request.method == "POST":
        # —– Botón de prueba de correo —–
        if request.form.get("accion") == "enviar_correo":
            prueba_email = request.form.get("test_email") or request.form.get("email")
            try:
                msg = Message(
                    subject="Correo de prueba",
                    recipients=[prueba_email],
                    html="<p>Este es un correo de prueba.</p>"
                )
                mail.send(msg)
                flash(f"Correo de prueba enviado a {prueba_email}", "success")
            except Exception as e:
                flash(f"Error al enviar correo de prueba: {e}", "danger")
            return redirect(url_for("estudiantes_bp.registro"))

        form = request.form
        email = form.get("email")

        try:
            # 1) Crea el colegio si es necesario
            school_name = (form.get("school_name") or "").strip()
            all_schools = GetAllSchools(school_repo).execute().schools
            matched = next(
                (s for s in all_schools if s.name.lower() == school_name.lower()),
                None
            )
            if not matched:
                matched = SchoolCreator(school_repo).execute(SchoolDTO(name=school_name))

            # 2) Crea al estudiante en BD (commit interno)
            student_dto = StudentDTO(
                first_name=form.get("first_name"),
                last_name=form.get("last_name"),
                email=email,
                password=form.get("password"),
                phone_number=form.get("phone_number"),
                ci=form.get("ci"),
                expedito_ci=form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(form.get("fecha_nacimiento"), "%Y-%m-%d"),
                school_id=matched.id,
                course=form.get("course"),
                department=form.get("department"),
                province=form.get("province"),
            )
            creado = StudentCreator(PostgresStudentRepository()).create_student(student_dto)
            # Aquí ya está creado el estudiante (si falla, irá directo al except)

            # 3) Enviar el correo de bienvenida **solo si la creación fue exitosa**
            msg = Message(
                subject="¡Bienvenido como Estudiante a EventMaker UMSS!",
                recipients=[email],
                html=render_template(
                    "emails/confirmacion_registro.html",
                    nombre=form.get("first_name"),
                    email=email,
                    rol="Estudiante"
                ),
                charset="utf-8"
            )
            mail.send(msg)

            # 4) Registrar la notificación en `notification`
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
                notification_type='confirmacion_registro_estudiante',
                status='sent'
            )
            log.sent_at = datetime.utcnow()
            db.session.add(log)
            db.session.commit()    # <- guarda el log en notificaciones

            flash("✓ Cuenta de estudiante creada exitosamente. Por favor revisa tu correo para confirmación.", "success")
            return redirect(url_for("admin_bp.login"))

        except smtplib.SMTPException as e:
            # Si falla el envío del correo, el estudiante YA ESTÁ CREADO en BD,
            # pero puedes mostrar el error y quizás ofrecer reintentar el correo
            flash(f"Error al enviar correo: {e}", "danger")
            return redirect(url_for("estudiantes_bp.registro"))

        except Exception as e:
            # Cualquier otro error (por ejemplo: validación fallida, error interno en StudentCreator)
            db.session.rollback()    # Se asegura de eliminar cualquier rastro parcial
            flash(f"Error inesperado: {e}", "danger")

            # Si existe un UserMapping intentando crearse (o Student), elimínalo para no dejar registro colgado
            posible_user = UserMapping.query.filter_by(email=email).first()
            if posible_user:
                db.session.delete(posible_user)
                db.session.commit()

            return redirect(url_for("estudiantes_bp.registro"))

    # GET → Mostrar formulario
    colegios = GetAllSchools(school_repo).execute().schools
    return render_template("students/registro.html", colegios=colegios)

@estudiantes_bp.route("/perfil", methods=["GET", "POST"])
def editar_perfil():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    # Obtener al estudiante
    repo = PostgresStudentRepository()
    student = repo.find_by_id(user_id)
    if not student:
        flash("No se encontró el perfil del estudiante", "danger")
        return redirect(url_for("home_bp.index"))

    user = UserMapping.query.get(user_id)

    # Obtener permisos
    permisos = []
    roles_usuario = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        udto = service.execute(role.id)
        if udto:
            if udto.permissions:
                permisos.extend(udto.permissions)
            if udto.name:
                roles_usuario.append(udto.name.lower())

    if request.method == "POST":
        try:
            student.first_name = request.form.get("first_name")
            student.last_name = request.form.get("last_name")
            student.ci = request.form.get("ci")
            student.expedito_ci = request.form.get("expedito_ci")
            student.fecha_nacimiento = request.form.get("fecha_nacimiento")
            student.phone_number = request.form.get("phone_number")
            student.course = request.form.get("course")
            student.department = request.form.get("department")
            student.province = request.form.get("province")

            # Guardar cambios
            repo.update(student)
            flash("Perfil actualizado correctamente", "success")
            return redirect(url_for("estudiantes_bp.editar_perfil"))
        except Exception as e:
            flash(str(e), "danger")

    dto = StudentDTO.from_domain(student)
    return render_template("perfil/editar_perfil_estudiante.html", student=dto, user=student,permisos=permisos,roles_usuario=roles_usuario)

