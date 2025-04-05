from flask import Blueprint, render_template, request, redirect, url_for, session
from modules.events.application.dtos.EventDTO import EventDTO
from modules.events.application.EventCreator import EventCreator
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from datetime import datetime

eventos_bp = Blueprint("eventos_bp", __name__, template_folder="views")

@eventos_bp.route("/crear", methods=["GET", "POST"])
def crear_evento():
    if request.method == "POST":
        # Obtener datos del formulario
        form = request.form
        afiche = request.files.get("imagen")

        user_id = session.get("admin_user")  # o el nombre de cookie que uses
        if not user_id:
            return redirect(url_for("admin_bp.login"))

        print("Tipo de evento:", form.get("tipo_evento"))

        event_dto = EventDTO(
            nombre_evento=form.get("titulo"),
            tipo_evento=form.get("tipo_evento") ,
            descripcion_evento=form.get("descripción"),
            inicio_evento=datetime.strptime(form.get("fecha_inicio"), "%Y-%m-%d"),
            fin_evento=datetime.strptime(form.get("fecha_fin"), "%Y-%m-%d"),
            capacidad_evento=int(form.get("capacidad")),
            inscripcion=form.get("Modalidad_inscripción"),
            requisitos=form.get("requisitos"),
            ubicacion=form.get("lugar"),
            slogan=form.get("mensaje"),
            afiche=afiche.read() if afiche else None,
            creador_id=[user_id]
        )

        repository = PostgresEventsRepository()
        creator = EventCreator(repository)
        creator.execute(event_dto)

        return redirect(url_for("admin_bp.dashboard"))

    return render_template("events/crearEvento.html")
