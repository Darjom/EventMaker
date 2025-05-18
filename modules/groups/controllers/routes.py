from flask import Blueprint,request, redirect, url_for, flash, render_template, session
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.events.application.EventQueryService import EventQueryService
from modules.groups.application.AssignGroupToTutor import AssignGroupToTutor
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.groups.application.GroupFinder import GroupFinder
from modules.delegations.application.GetTutorsByDelegation import GetTutorsByDelegation
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
grupos_bp = Blueprint("grupos_bp", __name__)

@grupos_bp.route("/grupos/<int:grupo_id>")
def ver_grupo(grupo_id):
    try:
        # Obtener datos del grupo
        finder = GroupFinder(PostgresGroupRepository())
        grupo_dto = finder.execute(grupo_id)

        # Obtener nombre del área
        delegacion_evento_id = EventQueryService(PostgresEventsRepository()).execute(grupo_dto.id_delegacion).id_evento
        areas_dto = AreaFinder(PostgresAreaRepository()).execute(delegacion_evento_id)
        area_dict = {area.id_area: area.nombre_area for area in areas_dto.areas}
        nombre_area = area_dict.get(grupo_dto.id_area, "Sin área asignada")
        # Obtener tutores de la delegación para el modal
        tutores_delegacion = GetTutorsByDelegation(
            PostgresDelegationRepository(),
            PostgresTutorRepository()
        ).execute(grupo_dto.id_delegacion)
        print(tutores_delegacion)
        return render_template("grupo/ver_grupo.html", grupo=grupo_dto, nombre_area=nombre_area,tutores_delegacion=tutores_delegacion)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("home_bp.index"))

@grupos_bp.route("/asignar-tutor", methods=["POST"])
def asignar_tutor_a_grupo():
    group_id = int(request.form.get("group_id"))
    tutor_id = int(request.form.get("tutor_id"))

    try:
        AssignGroupToTutor(PostgresGroupRepository()).execute(group_id, tutor_id)
        flash("Tutor asignado correctamente al grupo.", "success")
    except Exception as e:
        flash(f"Error al asignar tutor: {e}", "danger")

    # Obtener el grupo para redirigir correctamente
    grupo = GroupFinder(PostgresGroupRepository()).execute(group_id)
    return redirect(url_for("grupos_bp.ver_grupo", grupo_id=grupo.id_grupo))