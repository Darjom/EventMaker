from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from modules.areas.application.AreaFinder import AreaFinder
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.delegations.application.AssignTutorToDelegationByEmail import AssignTutorToDelegationByEmail
from modules.delegations.application.GetStudentByDelegation import GetStudentIdsByDelegation
from modules.events.application.EventQueryService import EventQueryService
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.delegations.application.dtos.DelegationDTO import DelegationDTO
from modules.delegations.application.DelegationCreator import DelegationCreator
from modules.delegations.application.TutorDelegationFinder import TutorDelegationsFinder
from modules.delegations.infrastructure.PostgresDelegationRepository import PostgresDelegationRepository
from modules.delegations.infrastructure.PostgresDelegationTutorRepository import PostgresDelegationTutorRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.delegations.application.AssignStudentToDelegationByEmail import AssignStudentToDelegationByEmail
from modules.delegations.application.GetTutorsByDelegation import GetTutorsByDelegation
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.students.application.StudentJoinDelegation import StudentJoinDelegation
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
from modules.groups.application.GroupCreator import GroupCreator
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.groups.application.dtos.GroupDTO import GroupDTO
from modules.delegations.application.FindDelegationById import FindDelegationById
from modules.tutors.application.GetTutorPermissionsInDelegation import GetTutorPermissionsInDelegation
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.groups.application.FindGroupsOfTutorInDelegation import FindGroupsOfTutorInDelegation
from modules.groups.infrastructure.PostgresGroupRepository import PostgresGroupRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository



delegaciones_bp = Blueprint("delegaciones_bp", __name__)


@delegaciones_bp.route("/crear-delegacion/<int:event_id>", methods=["GET", "POST"])
def crear_delegacion(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Validar que es tutor
    roles_usuario = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto and dto.name:
            roles_usuario.append(dto.name.lower())

    if "tutor" not in roles_usuario:
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("home_bp.index"))

    delegation_repo = PostgresDelegationRepository()
    tutor_repo = PostgresDelegationTutorRepository()

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre")
            codigo = request.form.get("codigo")

            if not nombre or not codigo:
                raise ValueError("Todos los campos son obligatorios")

            delegation_dto = DelegationDTO(
                nombre=nombre,
                evento_id=event_id,
                codigo=codigo
            )

            creator = DelegationCreator(delegation_repo, tutor_repo)
            creator.execute(delegation_dto, user_id)

            flash("Delegación creada correctamente", "success")
            return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

        except Exception as e:
            flash(str(e), "danger")

    evento = EventQueryService(PostgresEventsRepository()).execute(event_id)

    return render_template(
        "delegaciones/crear_delegacion.html",
        evento=evento,
        user=user,
        roles_usuario=roles_usuario
    )


@delegaciones_bp.route("/mis-delegaciones")
def mis_delegaciones():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener roles
    permisos = []
    roles_usuario = []
    for role in user.roles:
        service = RoleQueryService(PostgresRolesRepository())
        dto = service.execute(role.id)
        if dto:
            if dto.permissions:
                permisos.extend(dto.permissions)
            if dto.name:
                roles_usuario.append(dto.name.lower())

    finder = TutorDelegationsFinder(
        PostgresDelegationRepository(),
        PostgresDelegationTutorRepository()
    )

    try:
        delegaciones = finder.execute(user_id)
    except Exception as e:
        flash(str(e), "danger")
        delegaciones = []

    return render_template(
        "delegaciones/mis_delegaciones.html",
        delegaciones=delegaciones,
        user=user,
        permisos=permisos,
        roles_usuario=roles_usuario
    )


@delegaciones_bp.route("/ver-delegaciones")
def ver_delegaciones():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Verifica roles
    permisos = []
    roles_usuario = []
    for role in user.roles:
        dto = RoleQueryService(PostgresRolesRepository()).execute(role.id)
        if dto:
            if dto.permissions:
                permisos.extend(dto.permissions)
            if dto.name:
                roles_usuario.append(dto.name.lower())

    if "tutor" not in roles_usuario:
        flash("Acceso restringido", "danger")
        return redirect(url_for("home_bp.index"))

    # Buscar delegaciones asociadas
    finder = TutorDelegationsFinder(
        delegation_repo=PostgresDelegationRepository(),
        relation_repo=PostgresDelegationTutorRepository()
    )

    delegaciones = finder.execute(user_id)

    return render_template(
        "delegaciones/mis_delegaciones.html",
        delegaciones=delegaciones,
        user=user,
        permisos=permisos,
        roles_usuario=roles_usuario
    )
@delegaciones_bp.route("/delegacion/<int:delegacion_id>")
def ver_delegacion(delegacion_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener roles y permisos globales
    permisos = []
    roles_usuario = []
    for role in user.roles:
        dto = RoleQueryService(PostgresRolesRepository()).execute(role.id)
        if dto:
            if dto.permissions:
                permisos.extend(dto.permissions)
            if dto.name:
                roles_usuario.append(dto.name.lower())

    if "tutor" not in roles_usuario:
        flash("Acceso restringido", "danger")
        return redirect(url_for("home_bp.index"))

    try:
        # Obtener delegación
        finder = FindDelegationById(PostgresDelegationRepository())
        delegacion = finder.execute(delegacion_id)

        # Obtener estudiantes
        students_service = GetStudentIdsByDelegation(
            delegation_repository=PostgresDelegationRepository(),
            student_repository=PostgresStudentRepository()
        )
        estudiantes_dto = students_service.execute(delegacion_id)
        estudiantes = estudiantes_dto.students

        # Obtener tutores
        tutors_service = GetTutorsByDelegation(
            delegation_repository=PostgresDelegationRepository(),
            tutor_repository=PostgresTutorRepository()
        )
        tutores_dto = tutors_service.execute(delegacion_id)
        tutores = tutores_dto.tutors

        # ✅ Obtener permisos del tutor en la delegación
        permisos_delegacion = GetTutorPermissionsInDelegation(
            repository=PostgresTutorRepository()
        ).execute(tutor_id=user_id, delegation_id=delegacion_id)

        # Obtener grupos del tutor
        groups_dto = FindGroupsOfTutorInDelegation(
            repository=PostgresGroupRepository(),
            delegationTutor_repository=PostgresDelegationTutorRepository(),
            repository_user=PostgresUserRepository()
        ).execute(delegation_id=delegacion_id, tutor_id=user_id)

        # Obtener todas las áreas del evento asociado a la delegación
        areas_dto = AreaFinder(PostgresAreaRepository()).execute(delegacion.evento_id)
        areas_dict = {area.id_area: area.nombre_area for area in areas_dto.areas}

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("delegaciones_bp.ver_delegaciones"))

    # Debug
    print("Permisos globales:", permisos)
    print("Permisos en delegación:", permisos_delegacion)

    return render_template(
        "delegaciones/ver_delegacion.html",
        delegacion=delegacion,
        estudiantes=estudiantes,
        tutores=tutores,
        user=user,
        permisos=permisos,
        roles_usuario=roles_usuario,
        permisos_delegacion=permisos_delegacion,
        grupos=groups_dto.groups,
        areas_dict=areas_dict
    )



@delegaciones_bp.route('/delegaciones/<int:delegation_id>/agregar_estudiante', methods=['POST'])
def assign_student(delegation_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener correo del formulario
    email = request.form.get('email', '').strip()
    if not email:
        flash('Por favor ingrese un correo electrónico.', 'warning')
        return redirect(url_for('delegaciones_bp.ver_delegacion', delegacion_id=delegation_id))

    try:
        from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
        servicio = AssignStudentToDelegationByEmail(
            PostgresDelegationRepository(),
            PostgresUserRepository()
        )
        resultado = servicio.execute(delegation_id, email)

        if resultado == 0:
            flash(" No se encontró un usuario con ese correo.", "danger")
        elif resultado == 1:
            flash(" Estudiante agregado exitosamente a la delegación.", "success")
        elif resultado == 2:
            flash("️ El estudiante ya pertenece a esta delegación.", "warning")
        elif resultado == 3:
            flash(" El usuario no tiene el rol de estudiante.", "danger")
        else:
            flash(f" Resultado inesperado: {resultado}", "warning")
    except Exception as e:
        flash(f"Ocurrió un error al asignar el estudiante: {e}", "danger")

    return redirect(url_for('delegaciones_bp.ver_delegacion', delegacion_id=delegation_id))

@delegaciones_bp.route('/delegaciones/<int:delegation_id>/agregar_tutor', methods=['POST'])
def assign_tutor(delegation_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener correo del formulario
    email = request.form.get('email', '').strip()
    if not email:
        flash('Por favor ingrese un correo electrónico.', 'warning')
        return redirect(url_for('delegaciones_bp.ver_delegacion', delegacion_id=delegation_id))

    try:
        servicio = AssignTutorToDelegationByEmail(
            PostgresDelegationTutorRepository(),
            PostgresUserRepository()
        )
        resultado = servicio.execute(delegation_id, email)

        if resultado == AssignTutorToDelegationByEmail.USER_NOT_FOUND:
            flash(" No se encontró un usuario con ese correo.", "danger")
        elif resultado == AssignTutorToDelegationByEmail.USER_NOT_TUTOR:
            flash(" El usuario no tiene el rol de tutor.", "danger")
        elif resultado == AssignTutorToDelegationByEmail.SUCCESS:
            flash(" Tutor agregado exitosamente a la delegación.", "success")
        else:
            flash(f" Resultado inesperado: {resultado}", "warning")
    except Exception as e:
        flash(f"Ocurrió un error al asignar el tutor: {e}", "danger")

    return redirect(url_for('delegaciones_bp.ver_delegacion', delegacion_id=delegation_id))


@delegaciones_bp.route("/unirse-delegacion", methods=["GET", "POST"])
def unirse_delegacion():
    user_id = session.get("admin_user")  # ✅ mantenido como pediste
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # ✅ Validar que tenga el rol de estudiante
    roles_usuario = [role.name.lower() for role in user.roles]

    if "student" not in roles_usuario:
        flash("Acceso restringido a estudiantes.", "danger")
        return redirect(url_for("home_bp.index"))

    if request.method == "POST":
        codigo = request.form.get("codigo")

        servicio = StudentJoinDelegation(
            user_repository=PostgresUserRepository(),
            delegation_repository=PostgresDelegationRepository()
        )
        resultado = servicio.execute(code=codigo, student_id=user_id)

        if resultado == StudentJoinDelegation.USER_NOT_FOUND:
            flash("Usuario no encontrado.", "danger")
        elif resultado == StudentJoinDelegation.NOT_A_STUDENT:
            flash("Solo los estudiantes pueden unirse a una delegación.", "warning")
        elif resultado == StudentJoinDelegation.DELEGATION_NOT_FOUND:
            flash("No se encontró una delegación con ese código.", "danger")
        elif resultado == StudentJoinDelegation.ALREADY_ASSOCIATED:
            flash("Ya estás inscrito en esta delegación.", "info")
        elif resultado == StudentJoinDelegation.SUCCESSFULLY_ASSOCIATED:
            flash("Te uniste exitosamente a la delegación.", "success")

        return redirect(url_for("delegaciones_bp.unirse_delegacion"))

    return render_template(
        "delegaciones/unirse_delegacion.html",
        user=user,
        roles_usuario=roles_usuario
    )
@delegaciones_bp.route("/delegacion/<int:delegacion_id>/crear-grupo", methods=["GET", "POST"])
def crear_grupo(delegacion_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener permisos
    permisos = []
    for role in user.roles:
        dto = RoleQueryService(PostgresRolesRepository()).execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    # Obtener delegación y sus áreas
    delegacion = FindDelegationById(PostgresDelegationRepository()).execute(delegacion_id)
    evento = EventQueryService(PostgresEventsRepository()).execute(delegacion.evento_id)
    areas = AreaFinder(PostgresAreaRepository()).execute(evento.id_evento).areas

    if request.method == "POST":
        nombre = request.form.get("nombre_grupo")
        id_area = request.form.get("id_area")

        if not nombre or not id_area:
            flash("Debes llenar todos los campos.", "warning")
            return redirect(request.url)

        dto = GroupDTO(
            nombre_grupo=nombre,
            id_area=int(id_area),
            id_delegacion=delegacion_id
        )

        try:
            GroupCreator(PostgresGroupRepository()).execute(dto)
            flash("Grupo creado exitosamente.", "success")
            return redirect(url_for("delegaciones_bp.ver_delegacion", delegacion_id=delegacion_id))
        except Exception as e:
            flash(f"Error al crear grupo: {e}", "danger")
    return render_template(
        "grupo/crear_grupo.html",
        delegacion=delegacion,
        areas=areas,
        user=user,
        permisos=permisos
    )