from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
    return render_template("perfil/editar_perfil_estudiante.html", student=dto, user=student)

