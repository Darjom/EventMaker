# routes.py (de grupos)

from flask import Blueprint, render_template, flash, redirect, url_for
from modules.groups.application.GroupFinder import GroupFinder
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.events.application.EventQueryService import EventQueryService

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

        return render_template("grupo/ver_grupo.html", grupo=grupo_dto, nombre_area=nombre_area)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("home_bp.index"))
