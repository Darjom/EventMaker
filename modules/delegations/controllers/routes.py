from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.events.application.EventQueryService import EventQueryService
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.delegations.application.dtos.DelegationDTO import DelegationDTO
from modules.delegations.application.DelegationCreator import DelegationCreator
from modules.delegations.application.TutorDelegationFinder import TutorDelegationsFinder
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.delegations.infrastructure.PostgresDelegationTutorRepository import PostgresDelegationTutorRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping

delegaciones_bp = Blueprint("delegaciones_bp", __name__)


@delegaciones_bp.route("/crear-delegacion/<int:event_id>", methods=["GET", "POST"])
def crear_delegacion(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Validar que es tutor
    roles_usuario = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.name:
            roles_usuario.append(dto.name.lower())

    if "tutor" not in roles_usuario:
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("home_bp.index"))

    delegation_repo = PostgresDelegationRepository()
    tutor_repo = PostgresDelegationTutorRepository()

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre")
            codigo = request.form.get("codigo")

            if not nombre or not codigo:
                raise ValueError("Todos los campos son obligatorios")

            delegation_dto = DelegationDTO(
                nombre=nombre,
                evento_id=event_id,
                codigo=codigo
            )

            creator = DelegationCreator(delegation_repo, tutor_repo)
            creator.execute(delegation_dto, user_id)

            flash("Delegación creada correctamente", "success")
            return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

        except Exception as e:
            flash(str(e), "danger")

    evento = EventQueryService(PostgresEventsRepository()).execute(event_id)

    return render_template(
        "delegaciones/crear_delegacion.html",
        evento=evento,
        user=user,
        roles_usuario=roles_usuario
    )


@delegaciones_bp.route("/mis-delegaciones")
def mis_delegaciones():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener roles
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

    finder = TutorDelegationsFinder(
        PostgresDelegationRepository(),
        PostgresDelegationTutorRepository()
    )

    try:
        delegaciones = finder.execute(user_id)
    except Exception as e:
        flash(str(e), "danger")
        delegaciones = []

    return render_template(
        "delegaciones/mis_delegaciones.html",
        delegaciones=delegaciones,
        user=user,
        permisos=permisos,
        roles_usuario=roles_usuario
    )
