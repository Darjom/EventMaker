from flask import Blueprint,request, redirect, url_for, flash, render_template, session
from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.events.application.EventQueryService import EventQueryService
from modules.groups.application.AssignGroupToStudent import AssignGroupToStudent
from modules.groups.application.AssignGroupToTutor import AssignGroupToTutor
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.groups.application.GroupFinder import GroupFinder
from modules.delegations.application.GetTutorsByDelegation import GetTutorsByDelegation
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.groups.application.GroupFinder import GroupFinder
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.groups.application.GetStudentsOfGroup import GetStudentsOfGroup
from modules.groups.application.GetTutorsOfGroup import GetTutorsOfGroup
from modules.delegations.application.GetStudentByDelegation import GetStudentIdsByDelegation
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.inscriptions.application.BulkInscriptionsRegistrer import BulkInscriptionsRegistrar
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.categories.application.CategoryFinder import CategoryFinder
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.delegations.application.FindDelegationById import FindDelegationById

grupos_bp = Blueprint("grupos_bp", __name__)

@grupos_bp.route("/grupos/<int:grupo_id>")
def ver_grupo(grupo_id):
    print("estamos en la funcion de ver grupos")
    try:
        # Obtener datos del grupo
        finder = GroupFinder(PostgresGroupRepository())
        grupo_dto = finder.execute(grupo_id)

        #  Obtener delegación para acceder al evento_id
        delegacion_dto = FindDelegationById(PostgresDelegationRepository()).execute(grupo_dto.id_delegacion)

        # Obtener nombre del área
        areas_dto = AreaFinder(PostgresAreaRepository()).execute(delegacion_dto.evento_id)
        area_dict = {area.id_area: area.nombre_area for area in areas_dto.areas}
        nombre_area = area_dict.get(grupo_dto.id_area, "Sin área asignada")

        # Obtener estudiantes del grupo
        estudiantes = GetStudentsOfGroup(PostgresGroupRepository()).execute(grupo_id)

        # Obtener tutores del grupo
        tutores_grupo = GetTutorsOfGroup(PostgresGroupRepository()).execute(grupo_id)

        # Obtener tutores de la delegación (para asignar)
        tutores_delegacion = GetTutorsByDelegation(
            PostgresDelegationRepository(),
            PostgresTutorRepository()
        ).execute(grupo_dto.id_delegacion)

        estudiantes_delegacion = GetStudentIdsByDelegation(
            PostgresDelegationRepository(),
            PostgresStudentRepository()
        ).execute(grupo_dto.id_delegacion)

        categorias_dto = CategoryFinder(PostgresCategoryRepository()).execute(grupo_dto.id_area)
        return render_template(
            "grupo/ver_grupo.html",
            grupo=grupo_dto,
            delegacion=delegacion_dto,
            nombre_area=nombre_area,
            estudiantes=estudiantes,
            tutores_grupo=tutores_grupo,
            tutores_delegacion=tutores_delegacion,
            estudiantes_delegacion=estudiantes_delegacion,
            categorias=categorias_dto.categories
        )

    except Exception as e:
        flash(f"Error al ver grupo: {e}", "danger")
@grupos_bp.route("/asignar-tutor", methods=["POST"])
def asignar_tutor_a_grupo():
    group_id = int(request.form.get("group_id"))
    tutor_id = int(request.form.get("tutor_id"))

    try:
        AssignGroupToTutor(PostgresGroupRepository()).execute(group_id, tutor_id)
        flash("Tutor asignado correctamente al grupo.", "success")
    except Exception as e:
        flash(f"Error al asignar tutor: {e}", "danger")

    # Obtener el grupo para redirigir correctamente
    grupo = GroupFinder(PostgresGroupRepository()).execute(group_id)
    return redirect(url_for("grupos_bp.ver_grupo", grupo_id=grupo.id_grupo))

@grupos_bp.route("/asignar-estudiante", methods=["POST"])
def asignar_estudiante_a_grupo():
    try:
        group_id = int(request.form.get("group_id"))
        student_id = int(request.form.get("student_id"))

        AssignGroupToStudent(PostgresGroupRepository()).execute(group_id, student_id)
        flash("Estudiante asignado correctamente al grupo.", "success")
    except Exception as e:
        flash(f"Error al asignar estudiante: {e}", "danger")

    return redirect(url_for("grupos_bp.ver_grupo", grupo_id=group_id))

@grupos_bp.route("/inscribir-estudiantes", methods=["POST"])
def inscribir_estudiantes():
    try:
        group_id = int(request.form.get("group_id"))
        students_ids = request.form.getlist("students_ids")
        area_id = int(request.form.get("area_id"))
        category_id = int(request.form.get("category_id"))
        delegation_id = int(request.form.get("delegation_id"))
        event_id = int(request.form.get("event_id"))

        if not students_ids:
            flash("Debes seleccionar al menos un estudiante.", "warning")
            return redirect(url_for("grupos_bp.ver_grupo", grupo_id=group_id))

        students_ids = [int(sid) for sid in students_ids]

        servicio = BulkInscriptionsRegistrar(
            inscription_repository=PostgresInscriptionRepository(),
            student_repository=PostgresStudentRepository(),
            event_repository=PostgresEventsRepository(),
            area_repository=PostgresAreaRepository(),
            category_repository=PostgresCategoryRepository()
        )

        servicio.execute(
            students_ids=students_ids,
            event_id=event_id,
            area_id=area_id,
            category_id=category_id,
            delegation_id=delegation_id
        )

        flash("Estudiantes inscritos correctamente.", "success")

    except Exception as e:
        flash(f"Error al inscribir estudiantes: {e}", "danger")

    return redirect(url_for("grupos_bp.ver_grupo", grupo_id=group_id))