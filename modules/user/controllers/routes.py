from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.user.infrastructure.repositories import UserRepository
from modules.user.application.services import login_user

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    repo = UserRepository()
    token = login_user(email, password, repo)
    if not token:
        return jsonify({"msg": "Credenciales inválidas"}), 401

    return jsonify(access_token=token), 200

@user_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    identidad = get_jwt_identity()
    return jsonify({"msg": "Bienvenido", "user": identidad})
