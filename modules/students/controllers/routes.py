from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.application.StudentCreator import StudentCreator
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository

estudiantes_bp = Blueprint("estudiantes_bp", __name__)

@estudiantes_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        try:
            # Capturar datos del formulario
            student_dto = StudentDTO(
                first_name=request.form.get("first_name"),
                last_name=request.form.get("last_name"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                phone_number=request.form.get("phone_number"),
                ci=request.form.get("ci"),
                expedito_ci=request.form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(request.form.get("fecha_nacimiento"), "%Y-%m-%d"),
                school_id=int(request.form.get("school_id")),
                course=request.form.get("course"),
                department=request.form.get("department"),
                province=request.form.get("province"),
            )

            # Crear estudiante
            service = StudentCreator(PostgresStudentRepository())
            creado = service.create_student(student_dto)

            flash("Cuenta creada exitosamente. Por favor inicia sesión.", "success")
            return redirect(url_for("admin_bp.login"))

        except Exception as e:
            flash(str(e), "danger")

    return render_template("students/registro.html")
