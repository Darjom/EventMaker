from flask import Blueprint, render_template, request, redirect, url_for, session
from modules.admin.application.auth_service import authenticate_admin
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository

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
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    return render_template("admin/dashboard.html", user=user, permisos=permisos)

@admin_bp.route("/logout")
def logout():
    session.pop("admin_user", None)  # Elimina la cookie de sesión del usuario
    return redirect(url_for("admin_bp.login"))


