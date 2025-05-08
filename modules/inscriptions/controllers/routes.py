from flask import Blueprint, render_template, session, redirect, url_for, flash, request, send_file
from modules.events.application.EventQueryService import EventQueryService
from modules.areas.application.AreaFinder import AreaFinder
from modules.inscriptions.application.InscriptionRegister import InscriptionRegistrar
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.inscriptions.application.GetAllStudentInscriptions import GetAllStudentInscriptions
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.application.FindInscripPaymentStatusDelegation import FindInscripPaymentStatusDelegation
from modules.inscriptions.application.GetStudentInscriptionsByDelegation import GetStudentInscriptionsByDelegation
from modules.inscriptions.application.UpdateInscriptionStatus import UpdateInscriptionStatus
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.tutors.application.FindTutorById import FindTutorById
from modules.vouchers.infrastructure.PostgresVoucherRepository import PostgresVoucherRepository
from modules.vouchers.application.VoucherCreator import VoucherCreator
from modules.inscriptions.application.GenerateDelegationPaymentOrder import GenerateDelegationPaymentOrder

inscripciones_bp = Blueprint("inscripciones_bp", __name__)

@inscripciones_bp.route("/inscripcion/<int:event_id>", methods=["GET", "POST"])
def seleccionar_area_categoria(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener permisos del usuario
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

    if request.method == "POST":
        try:
            area_id = int(request.form.get("area_id"))
            category_id = int(request.form.get("category_id"))

            dto = InscriptionDTO(
                student_id=user_id,
                event_id=event_id,
                area_id=area_id,
                category_id=category_id
            )

            registrar = InscriptionRegistrar(
                inscription_repository=PostgresInscriptionRepository(),
                student_repository=PostgresStudentRepository(),
                event_repository=PostgresEventsRepository(),
                area_repository=PostgresAreaRepository(),
                category_repository=PostgresCategoryRepository()
            )

            registrar.execute(dto)
            flash("Inscripción realizada exitosamente", "success")
            return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

        except Exception as e:
            flash(str(e), "danger")

    event = EventQueryService(PostgresEventsRepository()).execute(event_id)
    areas = AreaFinder(PostgresAreaRepository()).execute(event_id).areas

    return render_template("inscripciones/form_inscripcion.html", evento=event, areas=areas, user=user, permisos=permisos,roles_usuario=roles_usuario)


@inscripciones_bp.route("/mis-inscripciones")
def ver_inscripciones_estudiante():
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Obtener permisos y roles
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

    # Instanciar caso de uso
    usecase = GetAllStudentInscriptions(
        inscription_repository=PostgresInscriptionRepository(),
        student_repository=PostgresStudentRepository(),
        event_repository=PostgresEventsRepository(),
        area_repository=PostgresAreaRepository(),
        category_repository=PostgresCategoryRepository()
    )

    try:
        inscripciones = usecase.execute(user_id)
    except Exception as e:
        flash(str(e), "danger")
        inscripciones = []

    return render_template("inscripciones/ver_inscripciones.html", inscripciones=inscripciones, user=user, permisos=permisos, roles_usuario=roles_usuario)

@inscripciones_bp.route("/orden-pago/evento/<int:event_id>", methods=["GET"])
def generar_orden_pago_estudiante(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    try:
        from modules.inscriptions.application.FindInscripPaymentStatusStudent import FindInscripPaymentStatusStudent

        servicio = FindInscripPaymentStatusStudent(
            repository=PostgresInscriptionRepository(),
            student_repository=PostgresStudentRepository(),
            event_repository=PostgresEventsRepository(),
            area_repository=PostgresAreaRepository(),
            category_repository=PostgresCategoryRepository(),
            voucher_repository=PostgresVoucherRepository()
        )

        pdf_buffer = servicio.execute(student_id=user_id, event_id=event_id)
        return send_file(pdf_buffer, as_attachment=True, download_name="orden_pago.pdf", mimetype="application/pdf")

    except Exception as e:
        flash(f"Error al generar la orden de pago: {str(e)}", "danger")
        return redirect(url_for("inscripciones_bp.ver_inscripciones_estudiante"))