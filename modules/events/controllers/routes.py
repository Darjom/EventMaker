from flask import Blueprint, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from modules.events.application.dtos.EventDTO import EventDTO
from modules.events.application.EventCreator import EventCreator
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from datetime import datetime
from modules.events.application.EventFinder import EventFinder
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.events.application.EventQueryService import EventQueryService
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from shared.ImageRotator import ImageRotator
from modules.events.application.EventDeleter import EventDeleter
eventos_bp = Blueprint("eventos_bp", __name__)

@eventos_bp.route("/crear", methods=["GET", "POST"])
def crear_evento():
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
        form = request.form
        file = request.files.get('afiche_path')
        titulo = form.get("titulo")

        # Validar si ya existe el evento
        repository = PostgresEventsRepository()
        finder = EventFinder(repository)
        existente = finder.by_name_and_user_id(titulo, user_id)

        if existente:
            flash("Ya existe un evento con ese nombre.", "error")
            return render_template("events/crearEvento.html", user=user, permisos=permisos)

        # Continuar con la creación
        file_path = None
        if file and file.filename != '':
            if not ImageRotator.is_allowed_file(file.filename):
                flash('Formato de imagen no permitido. Use JPG, PNG o WEBP', 'error')
                return render_template("events/crearEvento.html", user=user, permisos=permisos)

            file_path = ImageRotator.save_rotated_image(file)

        event_dto = EventDTO(
            nombre_evento=titulo,
            tipo_evento=form.get("tipo_evento"),
            descripcion_evento=form.get("descripcion"),
            inicio_evento=datetime.strptime(form.get("fecha_inicio"), "%Y-%m-%d"),
            fin_evento=datetime.strptime(form.get("fecha_fin"), "%Y-%m-%d"),
            inicio_inscripcion=datetime.strptime(form.get("fecha_inicio-inscripcion"), "%Y-%m-%d"),
            fin_inscripcion=datetime.strptime(form.get("fecha_fin-inscripcion"), "%Y-%m-%d"),
            capacidad_evento=int(form.get("capacidad")),
            inscripcion=form.get("tipo_evento"),
            requisitos=form.get("requisitos"),
            ubicacion=form.get("lugar"),
            slogan=form.get("slogan"),
            afiche=file_path,
            creador_id=[user_id]
        )

        creator = EventCreator(repository)
        creator.execute(event_dto)
        return redirect(url_for("admin_bp.dashboard"))
    return render_template("events/crearEvento.html", user=user, permisos=permisos)

@eventos_bp.route("/mis-eventos")
def mis_eventos():
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

    # Obtener los eventos del usuario
    from modules.events.application.UserEventFinder import UserEventFinder
    repository = PostgresEventsRepository()
    event_finder = UserEventFinder(repository)
    events_dto = event_finder.execute(user_id)

    return render_template("events/mis_eventos.html", user=user, permisos=permisos, eventos=events_dto.eventos)

@eventos_bp.route("/evento/<int:event_id>", methods=["GET"])
def ver_evento(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)
    # Obtener permisos del usuario
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

    repository = PostgresEventsRepository()
    service = EventQueryService(repository)
    evento = service.execute(event_id)

    if evento is None:
        return redirect(url_for("eventos_bp.mis_eventos"))
    # Obtener las áreas del evento
    area_finder = AreaFinder(PostgresAreaRepository())
    areas_dto = area_finder.execute(event_id)


    return render_template("events/ver_evento.html", evento=evento, user=user, permisos=permisos, areas=areas_dto.areas,roles_usuario=roles_usuario)

@eventos_bp.route("/evento/<int:event_id>/editar", methods=["GET", "POST"])
def editar_evento(event_id):
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

    repository = PostgresEventsRepository()
    service = EventQueryService(repository)
    evento = service.execute(event_id)

    if not evento:
        flash("Evento no encontrado.", "error")
        return redirect(url_for("eventos_bp.mis_eventos"))

    if request.method == "POST":
        form = request.form
        file = request.files.get('afiche_path')
        file_path = evento.afiche  # mantener el afiche actual por defecto

        if file and file.filename != '':
            if not ImageRotator.is_allowed_file(file.filename):
                flash('Formato de imagen no permitido. Use JPG, PNG o WEBP', 'error')
                return render_template("events/editarEvento.html", evento=evento, user=user, permisos=permisos)

            file_path = ImageRotator.save_rotated_image(file)

        from modules.events.application.EventUpdater import EventUpdater
        from modules.events.application.dtos.EventDTO import EventDTO

        dto = EventDTO(
            id_evento=event_id,
            nombre_evento=form.get("titulo"),
            tipo_evento=form.get("tipo_evento"),
            descripcion_evento=form.get("descripcion"),
            inicio_evento=datetime.strptime(form.get("fecha_inicio"), "%Y-%m-%d"),
            fin_evento=datetime.strptime(form.get("fecha_fin"), "%Y-%m-%d"),
            inicio_inscripcion=datetime.strptime(form.get("fecha_inicio-inscripcion"), "%Y-%m-%d"),
            fin_inscripcion=datetime.strptime(form.get("fecha_fin-inscripcion"), "%Y-%m-%d"),
            capacidad_evento=int(form.get("capacidad")),
            inscripcion=form.get("tipo_evento"),
            requisitos=form.get("requisitos"),
            ubicacion=form.get("lugar"),
            slogan=form.get("slogan"),
            afiche=file_path,
            creador_id=[user_id]
        )

        updater = EventUpdater(repository)
        updater.execute(dto)
        flash("Evento actualizado con éxito", "success")
        return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

    return render_template("events/editarEvento.html", evento=evento, user=user, permisos=permisos)


@eventos_bp.route("/evento/<int:event_id>/eliminar", methods=["POST"])
def eliminar_evento(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Verificar permisos
    permisos = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    if "event:delete" not in permisos:
        flash("No tienes permiso para eliminar este evento.", "error")
        return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

    # Eliminar el evento
    repository = PostgresEventsRepository()
    deleter = EventDeleter(repository)
    try:
        deleter.execute(event_id)
        flash("Evento eliminado correctamente.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar el evento: {str(e)}", "error")

    return redirect(url_for("eventos_bp.mis_eventos"))