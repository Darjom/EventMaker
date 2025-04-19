from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.events.application.EventQueryService import EventQueryService
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.areas.application.AreaFinder import AreaFinder
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.categories.application.CategoryFinder import CategoryFinder
from modules.inscriptions.application.InscriptionRegister import InscriptionRegistrar
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.user.infrastructure.persistence.UserMapping import UserMapping

inscripciones_bp = Blueprint("inscripciones_bp", __name__)

@inscripciones_bp.route("/inscripcion/<int:event_id>", methods=["GET", "POST"])
def seleccionar_area_categoria(event_id):
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

    if request.method == "POST":
        try:
            area_id = int(request.form.get("area_id"))
            category_id = int(request.form.get("category_id"))

            dto = InscriptionDTO(
                student_id=user_id,
                event_id=event_id,
                area_id=area_id,
                category_id=category_id
            )

            registrar = InscriptionRegistrar(
                inscription_repository=PostgresInscriptionRepository(),
                student_repository=PostgresStudentRepository(),
                event_repository=PostgresEventsRepository(),
                area_repository=PostgresAreaRepository(),
                category_repository=PostgresCategoryRepository()
            )

            registrar.execute(dto)
            flash("Inscripción realizada exitosamente", "success")
            return redirect(url_for("home_bp.index"))

        except Exception as e:
            flash(str(e), "danger")

    event = EventQueryService(PostgresEventsRepository()).execute(event_id)
    areas = AreaFinder(PostgresAreaRepository()).execute(event_id).areas

    return render_template("inscripciones/form_inscripcion.html", evento=event, areas=areas, user=user, permisos=permisos,roles_usuario=roles_usuario)
