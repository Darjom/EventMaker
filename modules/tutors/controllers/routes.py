from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from datetime import datetime

from modules.tutors.application.TutorCreator import TutorCreator
from modules.tutors.application.dtos.TutorDTO import TutorDTO
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository

tutores_bp = Blueprint("tutores_bp", __name__)

@tutores_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        form = request.form

        # Validación de contraseña
        if form.get("password") != form.get("confirm_password"):
            flash("Las contraseñas no coinciden.", "error")
            return render_template("tutors/registro.html")

        try:
            tutor_dto = TutorDTO(
                first_name=form.get("first_name"),
                last_name=form.get("last_name"),
                email=form.get("email"),
                password=form.get("password"),
                ci=form.get("ci"),
                expedito_ci=form.get("expedito_ci"),
                fecha_nacimiento=datetime.strptime(form.get("fecha_nacimiento"), "%Y-%m-%d")
            )

            creator = TutorCreator(PostgresTutorRepository())
            creator.create_tutor(tutor_dto)
            session.pop('_flashes', None)
            flash("Cuenta de tutor creada exitosamente.", "success")
            return redirect(url_for("admin_bp.login"))  # o a la página de login público

        except Exception as e:
            flash(str(e), "danger")
            return make_response(render_template("tutors/registro.html"))  # ✅
    response = make_response(render_template("tutors/registro.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
