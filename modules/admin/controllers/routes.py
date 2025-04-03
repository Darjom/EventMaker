from flask import Blueprint, render_template, request, redirect, url_for, session
from modules.admin.application.auth_service import authenticate_admin

admin_bp = Blueprint("admin_bp", __name__, template_folder="views")

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
    if not session.get("admin_user"):
        return redirect(url_for("admin_bp.login"))
    return "Bienvenido al Panel Administrativo"
