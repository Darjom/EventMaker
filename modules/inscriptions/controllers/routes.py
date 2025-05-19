import re

from flask import Blueprint, render_template, session, redirect, url_for, flash, request,send_file
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.events.application.EventQueryService import EventQueryService
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.areas.application.AreaFinder import AreaFinder
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.categories.application.CategoryFinder import CategoryFinder
from modules.inscriptions.application.GetStudentInscriptionsByEvent import GetStudentInscriptionsByEvent
from modules.inscriptions.application.StudentInscriptionValidator import StudentInscriptionValidator
from modules.inscriptions.application.InscriptionRegister import InscriptionRegistrar
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
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
from modules.vouchers.application.GetVoucherByInscriptions import GetVoucherByInscriptions
from modules.vouchers.application.VoucherUpdater import VoucherUpdater
from modules.vouchers.infrastructure.PostgresVoucherRepository import PostgresVoucherRepository
from modules.vouchers.application.VoucherCreator import VoucherCreator
from modules.inscriptions.application.GenerateDelegationPaymentOrder import GenerateDelegationPaymentOrder
from modules.OCR.application.PreprocesamientoOCRService import ImageProcessorService
from modules.OCR.application.ProcesamientoOCRService import ProcesadorOCR
from modules.OCR.application.ManejoArchivosService import GestorArchivosOriginales
from modules.OCR.application.OrquestadorOCRService import OrquestadorOCRService
from flask import Blueprint, render_template, flash, redirect, url_for
from modules.inscriptions.application.GetInscriptionsByEvent import GetInscriptionsByEvent
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.application.GetStudentById import GetStudentById
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.application.GetStudentInscriptionsByCategory import GetStudentInscriptionsByCategory
from modules.inscriptions.application.ExportStudentInscriptionsService import ExportStudentInscriptionsService
from modules.students.application.GetStudentById import GetStudentById
from modules.schools.application.FindSchoolById import FindSchoolById
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository

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

    # Recuperar resultado del OCR si existe
    ocr_resultado = None
    if "ocr_resultado" in session:
        ocr_resultado = session.get("ocr_resultado")
        session.pop("ocr_resultado")  # limpiar después de mostrar

    return render_template(
        "inscripciones/ver_inscripciones.html",
        inscripciones=inscripciones,
        user=user,
        permisos=permisos,
        roles_usuario=roles_usuario,
        ocr_resultado=ocr_resultado
    )

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

@inscripciones_bp.route("/comprobar-recibo/<int:event_id>", methods=["POST"])
def comprobar_recibo_ocr(event_id):
    try:
        # 1. Validar y obtener datos básicos
        student_id = session.get("admin_user") # Debug 2
        if not student_id: # Debug 3
            return redirect(url_for("admin_bp.login"))
         # Debug 4
        if 'recibo' not in request.files:  # Debug 5
            flash("No se envió ningún archivo", "danger")
            return redirect(url_for("inscripciones_bp.ver_inscripciones_estudiante"))

        file = request.files['recibo'] # Debug 6

        if file.filename == '':  # Debug 7
            flash("Archivo no seleccionado", "danger")
            return redirect(url_for("inscripciones_bp.ver_inscripciones_estudiante"))

        # 2. Configurar dependencias
        inscription_repo = PostgresInscriptionRepository()
        student_repo = PostgresStudentRepository()
        voucher_repo = PostgresVoucherRepository()
        area_repo=PostgresAreaRepository(),
        category_repo=PostgresCategoryRepository()
        # Instanciar OCR service con dependencias explícitas

        
        ocr_service = OrquestadorOCRService(
            gestor=GestorArchivosOriginales(),
            procesador_img=ImageProcessorService(),
            ocr_proc=ProcesadorOCR()
        )

        # 3. Instanciar servicios
        get_inscriptions_service = GetStudentInscriptionsByEvent(
            inscription_repo, 
            PostgresEventsRepository(),                   # EventRepository
            PostgresAreaRepository(),                     # AreaRepository
            PostgresCategoryRepository()                  # CategoryRepository
        )
        
        get_voucher_service = GetVoucherByInscriptions(voucher_repo)
        voucher_updater = VoucherUpdater(voucher_repo)
        update_status_service = UpdateInscriptionStatus(inscription_repo)

        # 4. Crear validador
        validator = StudentInscriptionValidator(
            ocr_service=ocr_service,
            get_inscriptions_service=get_inscriptions_service,
            get_voucher_service=get_voucher_service,
            voucher_updater=voucher_updater,
            update_status_service=update_status_service
        )

        # 5. Ejecutar validación
        result_message = validator.validate(
            image_invoice=file,  # Asegurar que el OCR acepte este formato
            event_id=event_id,
            student_id=student_id
        )

        # 6. Manejar resultado
        if "no es el mismo" in result_message:
            flash(result_message, "warning")
        else:
            flash(result_message, "success")

    except Exception as e:
        flash(f"Error en validación: {str(e)}", "danger")

    return redirect(url_for("inscripciones_bp.ver_inscripciones_estudiante"))


@inscripciones_bp.route("/evento/<int:event_id>/inscripciones")
def ver_inscripciones_evento(event_id):
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))

    user = UserMapping.query.get(user_id)

    # Verificar roles (admin o moderator)
    roles_usuario = []
    for role in user.roles:
        dto = RoleQueryService(PostgresRolesRepository()).execute(role.id)
        if dto and dto.name:
            roles_usuario.append(dto.name.lower())

    if "moderator" not in roles_usuario and "admin" not in roles_usuario:
        flash("Acceso restringido", "danger")
        return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))

    usecase = GetInscriptionsByEvent(
        PostgresInscriptionRepository(),
        GetStudentById(PostgresStudentRepository()),
        PostgresAreaRepository(),
        PostgresCategoryRepository()
    )

    try:
        datos = usecase.execute(event_id)
    except Exception as e:
        flash(f"Error al obtener inscripciones: {e}", "danger")
        return redirect(url_for("eventos_bp.ver_evento", event_id=event_id))


    evento = EventQueryService(PostgresEventsRepository()).execute(event_id)

    return render_template(
        "inscripciones/ver_inscripciones_por_evento.html",
        datos=datos,
        nombre_evento=evento.nombre_evento,
        user=user,
        event_id=event_id
    )


@inscripciones_bp.route("/evento/<int:event_id>/descargar-excel")
def descargar_reporte_excel(event_id):
    student_repo = PostgresStudentRepository()
    school_repo = PostgresSchoolRepository()
    category_repo = PostgresCategoryRepository()
    inscription_repo = PostgresInscriptionRepository()
    event_repo = PostgresEventsRepository()

    use_case = GetStudentInscriptionsByCategory(
        inscription_repo=inscription_repo,
        student_service=GetStudentById(student_repo),
        school_service=FindSchoolById(school_repo),
        category_service=category_repo
    )

    export_service = ExportStudentInscriptionsService(use_case, event_repo)

    try:
        excel_buffer = export_service.generate_excel(event_id)
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f"reporte_inscripciones.xlsx"
        )
    except Exception as e:
        flash(f"Error al generar el Excel: {str(e)}", "danger")
        return redirect(url_for("inscripciones_bp.ver_inscripciones_evento", event_id=event_id))


@inscripciones_bp.route("/evento/<int:event_id>/descargar-pdf")
def descargar_reporte_pdf(event_id):

    student_repo = PostgresStudentRepository()
    school_repo = PostgresSchoolRepository()
    category_repo = PostgresCategoryRepository()
    inscription_repo = PostgresInscriptionRepository()
    event_repo = PostgresEventsRepository()
 
    use_case = GetStudentInscriptionsByCategory(
        inscription_repo=inscription_repo,
        student_service=GetStudentById(student_repo),
        school_service=FindSchoolById(school_repo),
        category_service=category_repo
    )

    export_service = ExportStudentInscriptionsService(use_case, event_repo)

    pdf_buffer = export_service.generate_pdf(event_id)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"reporte_inscripciones_evento_{event_id}.pdf"
    )