from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from datetime import datetime

from flask_mail import Message
from shared.extensions import mail, db

from modules.tutors.application.TutorCreator import TutorCreator
from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

from modules.tutors.application.TutorStudentAssigner import TutorStudentAssigner
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository

tutores_bp = Blueprint("tutores_bp", __name__)

@tutores_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        form = request.form
        # Validación de contraseñas
        if form.get("password") != form.get("confirm_password"):
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("tutors/registro.html")

        email = form.get("email")
        # 1) Enviar correo de confirmación antes de tocar la DB
        try:
            msg = Message(
                subject="¡Bienvenido como Tutor a EventMaker UMSS!",
                recipients=[email],
                html=render_template(
                    "emails/confirmacion_registro.html",
                    nombre=form.get("first_name"),
                    email=email
                )
            )
            mail.send(msg)
        except Exception as e:
            flash(f"Error al enviar correo de confirmación: {e}", "danger")
            return render_template("tutors/registro.html")

        # 2) Si el correo se envió, crear el tutor
        try:
            tutor_dto = TutorDTO(
                first_name=form.get("first_name"),
                last_name=form.get("last_name"),
                email=email,
                password=form.get("password"),
                ci=form.get("ci"),
                expedito_ci=form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(form.get("fecha_nacimiento"), "%Y-%m-%d")
            )
            creator = TutorCreator(PostgresTutorRepository())
            creator.create_tutor(tutor_dto)
            flash("✓ Cuenta de tutor creada exitosamente. Por favor revisa tu correo para confirmación.", "success")
            return redirect(url_for("admin_bp.login"))
        except Exception as e:
            # Si hay un error al crear el tutor, intenta quitar cualquier dato huérfano
            flash(f"Error al crear cuenta de tutor: {e}", "danger")
            user = PostgresTutorRepository().find_by_email(email)
            if user:
                db.session.delete(user)
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
