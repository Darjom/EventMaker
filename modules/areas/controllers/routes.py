from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.areas.application.AreaCreator import AreaCreator
from modules.areas.application.dtos.AreaDTO import AreaDTO
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from flask import jsonify

areas_bp = Blueprint("areas_bp", __name__)


 # Añade esta importación

@areas_bp.route("/crear", methods=["GET", "POST"])
def crear_area():
    if request.method == "POST":
        try:
            imagen_file = request.files.get('imagen')

            # Validar campos obligatorios
            required_fields = ['titulo', 'descripcion', 'idevento']
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"El campo {field} es requerido.")

            # Obtener datos CORRECTAMENTE (sin comas y nombres correctos)
            nombre_area = request.form.get("titulo")  # String
            descripcion = request.form.get("descripcion")  # String
            id_evento = int(request.form.get("idevento"))  # Int
            afiche = imagen_file.read() if imagen_file else None  # Bytes o None

            # Crear DTO con los campos correctos
            area_dto = AreaDTO(
                nombre_area=nombre_area,
                descripcion=descripcion,
                id_evento=id_evento,
            )

            creator = AreaCreator(
                PostgresAreaRepository(),
                PostgresEventsRepository()
            )
            creator.execute(area_dto)

            return jsonify({"success": True, "message": "Área creada exitosamente!"})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    return render_template("areas/formCrearArea.html", evento_id=1)