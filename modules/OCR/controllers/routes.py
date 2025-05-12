from flask import Blueprint, render_template, redirect, url_for, session, request
from flask import current_app

# Servicios
from modules.OCR.application.PreprocesamientoOCRService import ImageProcessorService
from modules.OCR.application.ProcesamientoOCRService import ProcesadorOCR
from modules.OCR.application.ManejoArchivosService import GestorArchivosOriginales

# Módulos existentes
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository

ocr_bp = Blueprint("ocr_bp", __name__)

@ocr_bp.route('/ocr', methods=['GET', 'POST'])
def Prueba():
    with current_app.app_context():
        gestor_archivos = GestorArchivosOriginales()
    # Verificación de autenticación
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))
    
    user = UserMapping.query.get(user_id)
    if not user:
        return redirect(url_for("admin_bp.login"))
    
    # Inicializar servicios
    gestor_archivos = GestorArchivosOriginales()
    procesador_imagen = ImageProcessorService()
    ocr_processor = ProcesadorOCR()
    role_service = RoleQueryService(PostgresRolesRepository())

    error = None
    resultados = {}
    nombre_archivo = None
    previews = {}
    original_url = None

    if request.method == 'POST':
        file = request.files.get('file')
        nombre_archivo = None  # Inicializar aquí
        if file and file.filename:
            try:
                # 1. Guardar archivo original
                nombre_archivo = gestor_archivos.guardar_original(file)
                original_url = gestor_archivos.generar_url_original(nombre_archivo)
                
                # 2. Procesar imagen desde el archivo guardado
                ruta_original = gestor_archivos.obtener_ruta_original(nombre_archivo)
                with open(ruta_original, 'rb') as f:
                    img_procesada = procesador_imagen.process_uploaded_image(f)
                
                # 3. Recortar regiones en memoria
                numero_region = procesador_imagen.RecortarNumero(img_procesada)
                nombre_region = procesador_imagen.RecortarNombre(img_procesada)
                monto_region = procesador_imagen.RecortarMonto(img_procesada)
                
                # 4. Procesar OCR
                resultados = ocr_processor.procesar_todo(
                    procesador_imagen.preprocesar_para_ocr(numero_region),
                    procesador_imagen.preprocesar_para_ocr(nombre_region),
                    procesador_imagen.preprocesar_para_ocr(monto_region)
                )
                previews = {
                    'numero': gestor_archivos.generar_url_original(
                        gestor_archivos.guardar_preview(numero_region, 'numero')
                    ),
                    'nombre': gestor_archivos.generar_url_original(
                        gestor_archivos.guardar_preview(nombre_region, 'nombre')
                    ),
                    'monto': gestor_archivos.generar_url_original(
                        gestor_archivos.guardar_preview(monto_region, 'monto')
                    )
                        }
            except Exception as e:
                error = f"Error procesando imagen: {str(e)}"
                # Limpiar archivo original en caso de error
                if nombre_archivo:
                    gestor_archivos.eliminar_original(nombre_archivo)

    # Obtener permisos
    permisos = []
    for role in user.roles:
        dto = role_service.execute(role.id)
        if dto and dto.permissions:
            permisos.extend(dto.permissions)

    return render_template(
        "OCR/Prueba.html",
        user=user,
        permisos=permisos,
        role=user.roles[0] if user.roles else None,
        error=error,
        texto_numero=resultados.get('numero', ''),
        texto_nombre=resultados.get('nombre', ''),
        texto_monto=resultados.get('monto', ''),
        preview_numero=previews.get('numero'),
        preview_nombre=previews.get('nombre'),
        preview_monto=previews.get('monto'),
        original_url=original_url
    )