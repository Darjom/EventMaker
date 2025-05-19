from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

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

estudiantes_bp = Blueprint("estudiantes_bp", __name__)


@estudiantes_bp.route("/registro", methods=["GET", "POST"])
def registro():
    school_repo = PostgresSchoolRepository()

    if request.method == "POST":
        try:
            school_name = request.form.get("school_name").strip()
            school_service = GetAllSchools(school_repo)
            all_schools = school_service.execute().schools

            # Verificar si existe
            matched_school = next((s for s in all_schools if s.name.lower() == school_name.lower()), None)

            # Si no existe, crearla
            if not matched_school:
                nuevo_school_dto = SchoolDTO(name=school_name)
                school_creator = SchoolCreator(school_repo)
                matched_school = school_creator.execute(nuevo_school_dto)

            school_id = matched_school.id  # ahora sí tenemos el ID del colegio

            student_dto = StudentDTO(
                first_name=request.form.get("first_name"),
                last_name=request.form.get("last_name"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                phone_number=request.form.get("phone_number"),
                ci=request.form.get("ci"),
                expedito_ci=request.form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(request.form.get("fecha_nacimiento"), "%Y-%m-%d"),
                school_id=school_id,
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

    # GET → pasar colegios
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

