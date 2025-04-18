from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.categories.application.CategoryCreator import CategoryCreator
from modules.categories.application.dtos.CategoryDTO import CategoryDTO
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from flask import Blueprint, jsonify
from modules.categories.application.CategoryFinder import CategoryFinder
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository


categorias_bp = Blueprint("categorias_bp", __name__)

@categorias_bp.route("/crear/<int:area_id>", methods=["GET", "POST"])
def crear_categoria(area_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    permisos = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            precio_raw = request.form.get("precio")
            precio = int(precio_raw) if precio_raw else None

            dto = CategoryDTO(
                area_id=area_id,
                category_name=nombre,
                description=descripcion,
                price=precio
            )

            creator = CategoryCreator(
                PostgresCategoryRepository(),
                PostgresAreaRepository()
            )
            creator.execute(dto)
            flash("Categoría creada exitosamente", "success")
            return redirect(url_for("admin_bp.dashboard"))

        except Exception as e:
            flash(f"Error al crear categoría: {str(e)}", "danger")

    return render_template("categorias/formCrearCategoria.html", area_id=area_id,user=user,permisos=permisos)

@categorias_bp.route('/api/categorias/<int:area_id>')
def obtener_categorias_por_area(area_id):
    finder = CategoryFinder(PostgresCategoryRepository())
    categorias_dto = finder.execute(area_id)
    return jsonify([cat.model_dump() for cat in categorias_dto.categories])