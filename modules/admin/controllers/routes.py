from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from modules.admin.application.auth_service import authenticate_admin
from shared.extensions import db
from modules.user.infrastructure.persistence.UserMapping import UserMapping

admin_bp = Blueprint("admin_bp", __name__, template_folder="views")
tutor_bp = Blueprint("tutor_bp", __name__, template_folder="crearTutores")
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = authenticate_admin(email, password)
        if user:
            session["admin_user"] = user.id
            return redirect(url_for("admin_bp.dashboard"))
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@admin_bp.route("/dashboard")
def dashboard():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))
    return "Bienvenido al Panel Administrativo"

@tutor_bp.route("/CrearTutores", methods=["POST"])
def CrearTutor():
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'apellido' not in data or 'correo' not in data or 'contraseña' not in data:
            return jsonify({"error": "Datos incompletos"}), 400
        if Tutor.query.filter_by(email=data['correo']).first():
            return jsonify({"error": "El correo ya está registrado"}), 409
                # Crear nuevo tutor
        nuevo_tutor = Tutor(
            email=data['correo'],
            password_hash=hashed_password
        )
        
        db.session.add(nuevo_tutor)
        db.session.commit()
        
        return jsonify({"mensaje": "Tutor creado exitosamente", "id": nuevo_tutor.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    user = UserMapping.query.get(user_id)
    return render_template("dashboard.html", user=user)
