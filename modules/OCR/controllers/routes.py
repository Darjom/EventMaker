
from flask import Blueprint, render_template, redirect, url_for, session, request, url_for
import os
import pytesseract
from PIL import Image, ImageOps
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.roles.application.RoleQueryService import RoleQueryService
from modules.roles.infrastructure.PostgresRolesRepository import PostgresRolesRepository
import uuid
from io import BytesIO
import numpy as np
import cv2


ocr_bp = Blueprint("ocr_bp", __name__)

# Configurar la ruta de Tesseract si es necesario
# pytesseract.pytesseract.tesseract_cmd = r'RUTA_A_TESSERACT'

# Leer imagen

def recortarYRescalarImagen(img):
# 1. Redimensionamiento inicial
    resized = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
    
    # 2. Preprocesamiento para detección de bordes
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    # 3. Detección de contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 4. Parámetros de recorte
    img_height, img_width = resized.shape[:2]
    x, y, w, h = 0, 0, img_width, img_height  # Valores por defecto
    
    if contours:
        # Buscar el contorno más significativo
        main_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(main_contour)
        
        # Validación de bordes con tolerancia
        tolerancia = 10
        bordes_tocados = (
            x <= tolerancia or
            y <= tolerancia or
            (x + w) >= (img_width - tolerancia) or
            (y + h) >= (img_height - tolerancia)
        )
        
        if bordes_tocados:
            print("Advertencia: Contorno en bordes - Usando imagen completa")
            x, y, w, h = 0, 0, img_width, img_height
    
    # 5. Operación de recorte
    cropped = resized[y:y+h, x:x+w]
    
    # 6. Redimensionado final
    return cv2.resize(cropped, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)

def grisado(img):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gris

def rescalado(img):
    factor_escala=3
    rescalado=cv2.resize(img,
                   None,
                   fx=factor_escala,
                   fy=factor_escala,
                   interpolation=cv2.INTER_CUBIC)
    return rescalado

def nitidizacion(img):
    blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=3)
    nitido = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)
    return nitido

def binarizacion(img):
    _, binario = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binario

def preprocesado(img):
    gris=grisado(img)
    rescala=rescalado(gris)
    nitido=nitidizacion(rescala)
    binario=binarizacion(nitido)
    return binario

def RecortarNumero(img):
    """Recorta el área del número de la papeleta"""
    try:
        img=img[0:100, 1550:1920]
        return img
    except Exception as e:
        raise RuntimeError(f"Error recortando número: {str(e)}")

def RecortarNombre(img):
    """Recorta el área del nombre en la papeleta"""
    try:
        img=img[510:560, 330:1060]
        return img
    except Exception as e:
        raise RuntimeError(f"Error recortando nombre: {str(e)}")

def RecortarMonto(img):
    """Recorta el área del nombre en la papeleta"""
    try:
        img=img[630:690, 1750:1890]
        return img
    except Exception as e:
        raise RuntimeError(f"Error recortando monto: {str(e)}")

    
@ocr_bp.route('/ocr', methods=['GET', 'POST'])
def Prueba():
    # Verificación de autenticación
    user_id = session.get("admin_user")
    if not user_id:
        return redirect(url_for("admin_bp.login"))
    
    user = UserMapping.query.get(user_id)
    if not user:
        return redirect(url_for("admin_bp.login"))
    
    error = None
    permisos = []
    preview_numero = None
    preview_nombre = None
    preview_monto = None
    texto_numero = ""
    texto_nombre = ""
    texto_monto = ""
    numero_path = None
    nombre_path = None
    monto_path = None
    role_service = RoleQueryService(PostgresRolesRepository())

    if request.method == 'POST':
        file = request.files.get('file')
        
        if file and file.filename:
            try:
                # Procesar imagen
                img = Image.open(BytesIO(file.read()))
                img = ImageOps.exif_transpose(img)
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                img = recortarYRescalarImagen(img_cv)
            
            # Convertir resultado de OpenCV a PIL Image para los recortes
                numero=RecortarNumero(img)
                nombre=RecortarNombre(img)
                monto=RecortarMonto(img)
                # Guardar previews
                upload_dir = os.path.join('static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generar nombres únicos
                unique_id = uuid.uuid4().hex
                numero_path = os.path.join(upload_dir, f"numero_{unique_id}.jpg")
                nombre_path = os.path.join(upload_dir, f"nombre_{unique_id}.jpg")
                monto_path = os.path.join(upload_dir, f"monto_{unique_id}.jpg")

                cv2.imwrite(numero_path, numero)
                cv2.imwrite(nombre_path, nombre)
                cv2.imwrite(monto_path, monto)

                
                # Configurar URLs
                preview_numero = url_for('static', filename=f'uploads/numero_{unique_id}.jpg')
                preview_nombre = url_for('static', filename=f'uploads/nombre_{unique_id}.jpg')
                preview_monto = url_for('static', filename=f'uploads/monto_{unique_id}.jpg')
                cv2.imwrite("debug_numero_preprocesado.jpg", preprocesado(numero))
                
                # Extraer texto
                texto_numero = pytesseract.image_to_string(
                    preprocesado(numero),
                    lang='spa',
                    config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789.,'
                ).strip()
                
                texto_nombre = pytesseract.image_to_string(
                    preprocesado(nombre),
                    lang='spa',
                    config='--psm 6 --oem 3 '
                ).strip()

                texto_monto = pytesseract.image_to_string(
                    preprocesado(monto),
                    lang='spa',
                    config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789.,'
                ).strip()

            except Exception as e:
                error = f"Error procesando imagen: {str(e)}"
                # Limpiar archivos temporales en caso de error
                for path in [numero_path, nombre_path,monto_path]:
                    if path and os.path.exists(path):
                        os.remove(path)

    # Obtener permisos
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
        preview_numero=preview_numero,
        preview_nombre=preview_nombre,
        preview_monto=preview_monto,
        texto_numero=texto_numero,
        texto_nombre=texto_nombre,
        texto_monto=texto_monto
    )


