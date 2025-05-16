from flask import Blueprint, render_template

grupos_bp = Blueprint("grupos_bp", __name__)

@grupos_bp.route("/ver/<int:grupo_id>")
def ver_grupo(grupo_id):
    # lógica para obtener y mostrar el grupo
    return render_template("grupo/ver_grupo.html", grupo_id=grupo_id)
