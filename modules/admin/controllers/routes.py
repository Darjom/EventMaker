from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from modules.admin.application.auth_service import authenticate_admin
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.events.application.ActiveEventFinder import ActiveEventFinder
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.events.application.RandomActiveEventFinder import RandomActiveEventFinder
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.students.application.dtos.StudentDTO import StudentDTO

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = authenticate_admin(email, password)
        if user:
            session["admin_user"] = user.id
            return redirect(url_for("admin_bp.dashboard"))
        else:
            return render_template("admin/login.html", error="Credenciales inválidas")
    return render_template("admin/login.html")

@admin_bp.route("/dashboard")
def dashboard():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener permisos
    permisos = []
    roles_usuario = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto:
            if dto.permissions:
                permisos.extend(dto.permissions)
            if dto.name:
                roles_usuario.append(dto.name.lower())
    # Obtiene los 6 eventos aleatorios
    event_finder = RandomActiveEventFinder(PostgresEventsRepository())
    eventos_dto = event_finder.execute()

    return render_template("admin/dashboard.html", user=user, permisos=permisos,  eventos=eventos_dto.eventos, roles_usuario=roles_usuario)

@admin_bp.route("/logout")
def logout():
    session.pop("admin_user", None)  # Elimina la cookie de sesión del usuario
    return redirect(url_for("admin_bp.login"))

@admin_bp.route("/convocatorias-disponibles")
def convocatorias_disponibles():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    permisos = []
    roles_usuario = []

    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto:
            if dto.permissions:
                permisos.extend(dto.permissions)
            if dto.name:
                roles_usuario.append(dto.name.lower())

    finder = ActiveEventFinder(PostgresEventsRepository())
    eventos_dto = finder.execute()

    return render_template(
        "admin/convocatorias_disponibles.html",
        eventos=eventos_dto.eventos,
        user=user,
        permisos=permisos,
        roles_usuario=roles_usuario
    )
