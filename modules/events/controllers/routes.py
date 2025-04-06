from flask import Blueprint, render_template, request, redirect, url_for, session
from modules.events.application.dtos.EventDTO import EventDTO
from modules.events.application.EventCreator import EventCreator
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from datetime import datetime

from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.events.application.EventQueryService import EventQueryService

eventos_bp = Blueprint("eventos_bp", __name__)

@eventos_bp.route("/crear", methods=["GET", "POST"])
def crear_evento():
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

    if request.method == "POST":
        form = request.form
        afiche = request.files.get("afiche")

        event_dto = EventDTO(
            nombre_evento=form.get("titulo"),
            tipo_evento=form.get("tipo_evento"),
            descripcion_evento=form.get("descripcion"),
            inicio_evento=datetime.strptime(form.get("fecha_inicio"), "%Y-%m-%d"),
            fin_evento=datetime.strptime(form.get("fecha_fin"), "%Y-%m-%d"),
            capacidad_evento=int(form.get("capacidad")),
            inscripcion=form.get("tipo_evento"),  # Puedes modificarlo si usas otra lógica
            requisitos=form.get("requisitos"),
            ubicacion=form.get("lugar"),
            slogan=form.get("slogan"),
            afiche=afiche_path,
            creador_id=[user_id]
        )

        repository = PostgresEventsRepository()
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
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    repository = PostgresEventsRepository()
    service = EventQueryService(repository)
    evento = service.execute(event_id)

    if evento is None:
        return redirect(url_for("eventos_bp.mis_eventos"))

    return render_template("events/ver_evento.html", evento=evento, user=user, permisos=permisos)