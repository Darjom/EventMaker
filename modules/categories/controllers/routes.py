from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from modules.areas.application.AreaFinder import AreaFinder
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
from modules.categories.application.CategoryUpdater import CategoryUpdater

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


@categorias_bp.route("/editar/<int:category_id>", methods=["GET", "POST"])
def editar_categoria(category_id):
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

    # Repositorio de categorías
    category_repository = PostgresCategoryRepository()
    category_finder = CategoryFinder(category_repository)
    category_dto = category_finder.find_by_id(category_id)

    if not category_dto:
        flash("Categoría no encontrada", "danger")
        return redirect(url_for("admin_bp.dashboard"))

    # Repositorio de áreas
    area_repository = PostgresAreaRepository()
    area_finder = AreaFinder(area_repository)
    area_dto = area_finder.find_by_id(category_dto.area_id)

    if not area_dto:
        flash("Área relacionada no encontrada", "danger")
        return redirect(url_for("admin_bp.dashboard"))

    event_id = area_dto.id_evento

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            precio_raw = request.form.get("precio")
            precio = int(precio_raw) if precio_raw else None

            updated_dto = CategoryDTO(
                category_id=category_id,
                area_id=category_dto.area_id,
                category_name=nombre,
                description=descripcion,
                price=precio
            )

            updater = CategoryUpdater(category_repository)
            updater.execute(updated_dto)

            flash("Categoría actualizada exitosamente", "success")
            return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

        except Exception as e:
            import traceback
            traceback.print_exc()
            flash(f"Error al actualizar categoría: {str(e)}", "danger")

    return render_template(
        "categorias/formEditarCategoria.html",
        category=category_dto,
        user=user,
        permisos=permisos
    )
