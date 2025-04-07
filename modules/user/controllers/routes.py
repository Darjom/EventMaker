from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.roles.application.RolesQueryService import RolesQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.user.application.UserCreator import UserCreator
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.user.infrastructure.persistence.UserMapping import UserMapping

users_bp = Blueprint("users_bp", __name__)

@users_bp.route("/usuarios/crear", methods=["GET", "POST"])
def crear_usuario():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    permisos = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    roles_service = RolesQueryService(PostgresRolesRepository())
    roles_dto = roles_service.execute()

    if request.method == "POST":
        form = request.form
        rol_id = int(form.get("TipoDeUsuarios"))
        creator = UserCreator(
            user_repo=PostgresUserRepository(),
            role_query_service=RoleQueryService(PostgresRolesRepository())
        )
        nuevo = creator.execute(
            role_ids=[rol_id],
            first_name=form.get("nombre"),
            last_name=form.get("apellido"),
            email=form.get("correo"),
            password=form.get("contraseña")
        )
        flash("Usuario creado correctamente", "success")
        return redirect(url_for("admin_bp.dashboard"))

    return render_template(
        "admin/crearUser.html",
        roles=roles_dto.roles,
        user=user,
        permisos=permisos
    )