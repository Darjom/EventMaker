

from flask import Flask, session
from sqlalchemy import text

from config import Config
from modules.Data.RolesAndPermissions.Seeder import seed_roles_and_permissions

from modules.admin.controllers.routes import admin_bp
from modules.areas.controllers.routes import areas_bp
#from.modules.roles.controllers.routes import rol_bp
from shared.extensions import db, migrate, jwt, mail
from modules.home.controllers.routes import home_bp
from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from werkzeug.security import generate_password_hash
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.permissions.infrastructure.persistence.PermissionMapping import PermissionMapping
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.areas.infrastructure.persistence.AreaMapping import AreaMapping
from modules.categories.infrastructure.persistence.CategoryMapping import CategoryMapping
from modules.students.infrastructure.persistence.StudentMapping import StudentMapping
from modules.schools.infrastructure.persistence.SchoolMapping import SchoolMapping
from modules.inscriptions.infrastructure.persistence.InscriptionMapping import InscriptionMapping
from modules.tutors.infrastructure.persistence.TieneACargoMapping import TieneAcargoMapping
from modules.delegations.infrastructure.persistence.DelegationMapping import DelegationMapping
from modules.delegations.infrastructure.persistence.DelegationTutorMapping import DelegationTutorMapping
from modules.groups.infrastructure.persistence.GroupMapping import GroupMapping
from modules.vouchers.infrastructure.persistence.VoucherMapping import VoucherMapping
from modules.notifications.infrastructure.persistence.NotificationMapping import NotificationMapping
from modules.bitacoras.infrastructure.AuditLogMapping import AuditLogMapping
import uuid
from datetime import datetime
from modules.events.controllers.routes import eventos_bp
from modules.user.controllers.routes import users_bp
from modules.info.controllers.routes import info_bp
from modules.students.controllers.routes import estudiantes_bp
from modules.tutors.controllers.routes import tutores_bp
from modules.inscriptions.controllers.routes import inscripciones_bp
from modules.OCR.controllers.routes import ocr_bp
from modules.delegations.controllers.routes import delegaciones_bp
from modules.groups.controllers.routes import grupos_bp
from modules.categories.controllers.routes import categorias_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Crear las tablas si no existen
    #with app.app_context():
       # db.create_all()
    # Inserta datos de roles y permisos
    #seed_roles_and_permissions()

    # cargar colegios
    #from modules.Data.DatosColegios.cargar_colegios import CargarColegios
    #cargador = CargarColegios()
    #cargador.main()

    # user_id para bitacoras


    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(eventos_bp, url_prefix="/eventos")
    app.register_blueprint(areas_bp ,url_prefix="/area")
    app.register_blueprint(users_bp)
    app.register_blueprint(estudiantes_bp, url_prefix="/estudiantes")
    app.register_blueprint(tutores_bp, url_prefix="/tutores")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(inscripciones_bp, url_prefix="/inscripciones")
    app.register_blueprint(ocr_bp)
    app.register_blueprint(delegaciones_bp, url_prefix="/delegaciones")
    app.register_blueprint(info_bp)
    app.register_blueprint(grupos_bp, url_prefix="/grupos")


# Obtenemos el id_user para las bitacoras
    @app.before_request
    def set_user_id():
        # Suponiendo que has autenticado al usuario y tienes su ID
        user_id = session.get("admin_user")  # puedes usar 'request.user.id' o como lo manejes
        if user_id:
            db.session.execute(text(f"SET app.user_id = '{user_id}'"))

    return app



app = create_app()

if __name__ == "__main__":
    app.run()
