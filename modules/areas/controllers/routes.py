from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.areas.application.AreaCreator import AreaCreator
from modules.areas.application.AreaUpdater import AreaUpdater
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.ImageRotator import ImageRotator
from modules.areas.application.AreaFinder import AreaFinder


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
            file = request.files.get('imagen')
            file_path = None

            if file and file.filename != '':
                if not ImageRotator.is_allowed_file(file.filename):
                    flash('Formato de imagen no permitido. Use JPG, PNG o WEBP', 'error')
                    return render_template("areas/formCrearArea.html", user=user, permisos=permisos,
                                           evento_id=evento_id)

                file_path = ImageRotator.save_rotated_image(file)

            required_fields = ['titulo', 'descripcion']
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"El campo {field} es requerido.")

            nombre_area = request.form.get("titulo")
            descripcion = request.form.get("descripcion")

            # Validar si ya existe una área con el mismo nombre en el evento
            area_finder = AreaFinder(PostgresAreaRepository())
            area_existente = area_finder.by_name_and_event_id(nombre_area, evento_id)

            if area_existente:
                flash("❗ Ya existe un área con ese nombre para este evento.", "warning")
                return render_template("areas/formCrearArea.html", user=user, permisos=permisos, evento_id=evento_id)

            #  Crear el área si no existe
            area_dto = AreaDTO(
                nombre_area=nombre_area,
                descripcion=descripcion,
                id_evento=evento_id,
                afiche=file_path,
            )

            creator = AreaCreator(PostgresAreaRepository(), PostgresEventsRepository())
            creator.execute(area_dto)

            flash("Área creada exitosamente.", "success")
            return redirect(url_for("eventos_bp.ver_evento", event_id=evento_id))

        except Exception as e:
            flash(f"Error al crear el área: {str(e)}", "danger")

    return render_template(
        "areas/formCrearArea.html",
        user=user,
        permisos=permisos,
        evento_id=evento_id
    )

@areas_bp.route("/editar/<int:area_id>", methods=["GET", "POST"])
def editar_area(area_id):
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

    repository = PostgresAreaRepository()
    area = repository.find_by_id(area_id)

    if not area:
        flash("Área no encontrada", "danger")
        return redirect(url_for("eventos_bp.dashboard_admin"))

    if request.method == "POST":
        try:
            file = request.files.get('imagen')
            file_path = area.afiche  # por defecto, mantener el anterior

            if file and file.filename != '':
                if not ImageRotator.is_allowed_file(file.filename):
                    flash('Formato de imagen no permitido. Use JPG, PNG o WEBP', 'error')
                    return render_template("areas/formEditarArea.html", user=user, permisos=permisos, area=area)

                file_path = ImageRotator.save_rotated_image(file)

            nombre_area = request.form.get("titulo")
            descripcion = request.form.get("descripcion")

            dto = AreaDTO(
                id_area=area.id_area,
                nombre_area=nombre_area,
                descripcion=descripcion,
                id_evento=area.id_evento,
                afiche=file_path
            )

            updater = AreaUpdater(repository)
            updater.execute(dto)

            flash("Área actualizada exitosamente.", "success")
            return redirect(url_for("eventos_bp.ver_evento", event_id=area.id_evento))

        except Exception as e:
            flash(f"Error al actualizar el área: {str(e)}", "danger")

    return render_template("areas/formEditarArea.html", user=user, permisos=permisos, area=area)


