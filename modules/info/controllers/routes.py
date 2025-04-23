
from flask import Blueprint, render_template, redirect, url_for, session
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository

info_bp = Blueprint("info_bp", __name__)

@info_bp.route('/mi-informacion', methods=['GET'])
def Mi_Informacion():
    # Verificar si el usuario está autenticado
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))
    
    # Obtener datos del usuario desde la base de datos
    user = UserMapping.query.get(user_id)
    
    if not user:
        return redirect(url_for("admin_bp.login"))
    permisos = []
    role_service = RoleQueryService(PostgresRolesRepository())  # Una sola instancia
    for role in user.roles:
        dto = role_service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)
        # 4. Renderiza la plantilla pasando el objeto user y la lista de permisos
    return render_template(
        "info/Mi_Informacion.html",
        user=user,
        permisos=permisos,
        role=role
    )