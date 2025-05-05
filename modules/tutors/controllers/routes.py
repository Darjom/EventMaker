from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

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

        # Validación de contraseña
        if form.get("password") != form.get("confirm_password"):
            flash("Las contraseñas no coinciden.", "error")
            return render_template("tutors/registro.html")

        try:
            tutor_dto = TutorDTO(
                first_name=form.get("first_name"),
                last_name=form.get("last_name"),
                email=form.get("email"),
                password=form.get("password"),
                ci=form.get("ci"),
                expedito_ci=form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(form.get("fecha_nacimiento"), "%Y-%m-%d")
            )

            creator = TutorCreator(PostgresTutorRepository())
            creator.create_tutor(tutor_dto)

            flash("Cuenta de tutor creada exitosamente.", "success")
            return redirect(url_for("admin_bp.login"))  # o a la página de login público

        except Exception as e:
            flash(str(e), "danger")

    return render_template("tutors/registro.html")

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

    # Buscar al estudiante por correo electrónico
    student_repo = PostgresStudentRepository()
    student = student_repo.find_by_email(student_email)
    if not student:
        flash("No se encontró un estudiante con ese correo electrónico.", "danger")
        return redirect(url_for("tutores_bp.dashboard"))

    # Asignar el estudiante al tutor
    assigner = TutorStudentAssigner(PostgresTutorRepository())
    try:
        assigner.execute(student_id=student.id, tutor_id=tutor_id)
        flash("Estudiante agregado exitosamente.", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("tutores_bp.dashboard"))
