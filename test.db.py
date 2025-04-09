from werkzeug.security import generate_password_hash
from app import create_app
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db

# Crear la aplicación y contexto
app = create_app()
app.app_context().push()

def crear_usuario():
    # Datos del usuario
    id="3"
    first_name = "Ana"
    last_name = "Pérez"
    email = "ana@example.com"
    password = "123456"
    active=True


    # Generar hash de la contraseña
    password_hash = generate_password_hash(password)

    # Crear objeto de usuario
    nuevo_usuario = UserMapping(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password_hash,
        active=active
    )

    # Añadir a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()
    print(f"✅ Usuario {email} creado exitosamente.")

if __name__ == "__main__":
    crear_usuario()