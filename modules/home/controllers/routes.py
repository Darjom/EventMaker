from flask import Blueprint, render_template

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def index():
    return render_template("home/index.html", title="EventMaker")

@home_bp.route("/eventos")
def eventos():
    return "<h2>Página de eventos</h2>"  # Puedes renderizar un HTML más adelante

@home_bp.route("/ayuda")
def ayuda():
    return "<h2>Página de ayuda</h2>"

@home_bp.route("/contactos")
def contactos():
    return "<h2>Página de contactos</h2>"
