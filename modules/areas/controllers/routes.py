from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.areas.application.AreaCreator import AreaCreator
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping

areas_bp = Blueprint("areas_bp", __name__)

@areas_bp.route("/crear/<int:evento_id>", methods=["GET", "POST"])
def crear_area(evento_id):
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

    if request.method == "POST":
        try:
            imagen_file = request.files.get('imagen')

            required_fields = ['titulo', 'descripcion']
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"El campo {field} es requerido.")

            nombre_area = request.form.get("titulo")
            descripcion = request.form.get("descripcion")
            afiche = imagen_file.read() if imagen_file else None

            area_dto = AreaDTO(
                nombre_area=nombre_area,
                descripcion=descripcion,
                id_evento=evento_id,
            )

            creator = AreaCreator(
                PostgresAreaRepository(),
                PostgresEventsRepository()
            )
            creator.execute(area_dto)

            flash("Área creada exitosamente.", "success")
            return redirect(url_for("areas_bp.crear_area", evento_id=evento_id))

        except Exception as e:
            flash(f"Error al crear el área: {str(e)}", "danger")

    return render_template(
        "areas/formCrearArea.html",
        user=user,
        permisos=permisos,
        evento_id=evento_id
    )
