
from flask import Blueprint, render_template, redirect, url_for, session, request, url_for
import os
import pytesseract
from PIL import Image, ImageOps,ImageEnhance
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

def RecortarNumero(pil_img: Image.Image) -> Image.Image:
    """Recorta el área del número de la papeleta"""
    try:
        x1, y1, x2, y2 = 1080, 40, 1280, 95
        return pil_img.crop((x1, y1, x2, y2))
    except Exception as e:
        raise RuntimeError(f"Error recortando número: {str(e)}")

def RecortarNombre(pil_img: Image.Image) -> Image.Image:
    """Recorta el área del nombre en la papeleta"""
    try:
        x1, y1, x2, y2 = 190, 440, 620, 480
        return pil_img.crop((x1, y1, x2, y2))
    except Exception as e:
        raise RuntimeError(f"Error recortando nombre: {str(e)}")
    
def mejorar_calidad_nombre(img: Image.Image) -> Image.Image:
    """Preprocesamiento específico para nombres"""
    try:
        # Aumentar resolución
        img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
        
        # Convertir a escala de grises
        gray = img.convert("L")
        
        # Mejorar contraste
        enhancer = ImageEnhance.Contrast(gray)
        contrast_img = enhancer.enhance(3.0)
        
        # Reducción de ruido adaptativo
        np_img = np.array(contrast_img)
        denoised = cv2.fastNlMeansDenoising(np_img, h=15, templateWindowSize=7, searchWindowSize=21)
        
        # Umbralización adaptativa
        threshold_img = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 21, 8
        )
        
        # Dilatación para unir caracteres rotos
        kernel = np.ones((2, 1), np.uint8)  # Kernel vertical para mantener espacios
        dilated = cv2.dilate(threshold_img, kernel, iterations=1)
        
        return Image.fromarray(dilated)
    
    except Exception as e:
        raise RuntimeError(f"Error procesando nombre: {str(e)}")    

def limpiar_trazas_nombre(img: Image.Image) -> Image.Image:
    """Elimina trazas negras alrededor del texto"""
    try:
        # Convertir a array OpenCV
        img_np = np.array(img.convert("RGB"))
        
        # 1. Convertir a escala de grises
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # 2. Eliminar ruido con filtro bilateral
        denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
        
        # 3. Umbralización adaptativa para aislar texto
        thresh = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 21, 12
        )
        
        # 4. Operación morfológica para eliminar trazas pequeñas
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # 5. Invertir para tener texto negro sobre fondo blanco
        result = cv2.bitwise_not(cleaned)
        
        return Image.fromarray(result)
    
    except Exception as e:
        raise RuntimeError(f"Error limpiando trazas: {str(e)}")
    
def RecortarMonto(pil_img: Image.Image) -> Image.Image:
    """Recorta el área del nombre en la papeleta"""
    try:
        x1, y1, x2, y2 = 1190,570,1275,600
        return pil_img.crop((x1, y1, x2, y2))
    except Exception as e:
        raise RuntimeError(f"Error recortando monto: {str(e)}")
        
def mejorar_calidad_monto(img: Image.Image) -> Image.Image:
    """Optimiza la imagen del monto para OCR"""
    try:
        # Convertir a escala de grises
        gray = img.convert("L")
        
        # Aumentar contraste
        enhancer = ImageEnhance.Contrast(gray)
        contrast_img = enhancer.enhance(3.0)
        
        # Umbralización agresiva
        threshold_img = contrast_img.point(lambda x: 0 if x < 200 else 255)
        
        return threshold_img
    except Exception as e:
        raise RuntimeError(f"Error procesando monto: {str(e)}")
    
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
    role_service = RoleQueryService(PostgresRolesRepository())

    if request.method == 'POST':
        file = request.files.get('file')
        
        if file and file.filename:
            try:
                # Procesar imagen
                img = Image.open(BytesIO(file.read()))
                img = ImageOps.exif_transpose(img)
                
                # Recortar elementos
                numero_img = RecortarNumero(img)
                nombre_img = RecortarNombre(img)
                nombre_procesado = mejorar_calidad_nombre(nombre_img)
                monto_img = RecortarMonto(img)
                monto_procesado = mejorar_calidad_monto(monto_img)
                # Guardar previews
                upload_dir = os.path.join('static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generar nombres únicos
                unique_id = uuid.uuid4().hex
                numero_path = os.path.join(upload_dir, f"numero_{unique_id}.jpg")
                nombre_path = os.path.join(upload_dir, f"nombre_{unique_id}.jpg")
                monto_path = os.path.join(upload_dir, f"monto_{unique_id}.jpg")

                numero_img.save(numero_path)
                nombre_procesado.save(nombre_path)
                monto_procesado.save(monto_path)

                
                # Configurar URLs
                preview_numero = url_for('static', filename=f'uploads/numero_{unique_id}.jpg')
                preview_nombre = url_for('static', filename=f'uploads/nombre_{unique_id}.jpg')
                preview_monto = url_for('static', filename=f'uploads/monto_{unique_id}.jpg')
                
                # Extraer texto
                texto_numero = pytesseract.image_to_string(
                    numero_img,
                    lang='spa',
                    config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
                ).strip()
                
                texto_nombre = pytesseract.image_to_string(
                    nombre_img,
                    lang='spa',
                    config='--psm 6 --oem 3 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜ '
                ).strip()

                texto_monto = pytesseract.image_to_string(
                    monto_img,
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


