from flask import Blueprint, render_template, redirect, url_for
from modules.events.application.ActiveEventFinder import ActiveEventFinder
from modules.events.application.EventQueryService import EventQueryService
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository


home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def index():
    return render_template("home/index.html", title="EventMaker")

@home_bp.route("/eventos", methods=["GET"])
def eventos():
    repository = PostgresEventsRepository()
    finder = ActiveEventFinder(repository)
    eventos_dto = finder.execute()
    return render_template("home/todos_eventos.html", eventos=eventos_dto.eventos)

@home_bp.route("/evento/<int:event_id>")
def evento_publico(event_id):
    repository = PostgresEventsRepository()
    service = EventQueryService(repository)
    evento = service.execute(event_id)

    if not evento:
        return redirect(url_for("home_bp.eventos"))

    area_finder = AreaFinder(PostgresAreaRepository())
    areas_dto = area_finder.execute(event_id)

    return render_template("home/ver_evento_publico.html", evento=evento,areas=areas_dto.areas)
@home_bp.route("/ayuda")
def ayuda():
    return render_template("home/ayuda.html")

@home_bp.route("/contactos")
def contactos():
    return render_template("home/contactos.html")

