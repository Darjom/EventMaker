from flask import Flask
from config import Config
from modules.admin.controllers.routes import admin_bp
from shared.extensions import db, migrate, jwt
from modules.user.controllers.routes import user_bp
from modules.home.controllers.routes import home_bp
from modules.admin.infrastructure.admin_interface import init_admin
from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from werkzeug.security import generate_password_hash
from shared.extensions import db
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.permissions.infrastructure.persistence.PermissionMapping import PermissionMapping
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.areas.infrastructure.persistence.AreaMapping import AreaMapping
from modules.categories.infrastructure.persistence.CategoryMapping import CategoryMapping
import uuid
from datetime import datetime

def insert_admin_user():
    email = "admin@eventmaker.com"
    password = "admin123"  # 📌 Podés cambiarla
    hashed_password = generate_password_hash(password)

    # Verificar si ya existe
    if UserMapping.query.filter_by(email=email).first():
        print("⚠️ El usuario ya existe.")
        return

    # Obtener rol administrativo
    admin_role = RolMapping.query.filter_by(name="administrativo").first()
    if not admin_role:
        print("❌ No se encontró el rol 'administrativo'.")
        return

    # Crear nuevo usuario
    new_user = UserMapping(
        first_name="Admin",
        last_name="Root",
        email=email,
        password=hashed_password,
        active=True,
        confirmed_at=datetime.utcnow(),
        fs_uniquifier=str(uuid.uuid4()),
        roles=[admin_role]
    )

    db.session.add(new_user)
    db.session.commit()
    print("✅ Usuario administrador creado con éxito.")

def insert_default_roles():
    roles = [
        {"name": "administrativo", "description": "Admin del sistema"},
    ]

    for role in roles:
        exists = RolMapping.query.filter_by(name=role["name"]).first()
        if not exists:
            db.session.add(RolMapping(name=role["name"], description=role["description"]))
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()
        insert_default_roles()
        insert_admin_user()

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    init_admin(app)

    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
