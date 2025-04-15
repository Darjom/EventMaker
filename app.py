from flask import Flask
from config import Config
from modules.admin.controllers.routes import admin_bp
from modules.areas.controllers.routes import areas_bp
#from.modules.roles.controllers.routes import rol_bp
from shared.extensions import db, migrate, jwt
from modules.home.controllers.routes import home_bp
from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from werkzeug.security import generate_password_hash
from shared.extensions import db
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from modules.permissions.infrastructure.persistence.PermissionMapping import PermissionMapping
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.areas.infrastructure.persistence.AreaMapping import AreaMapping
from modules.categories.infrastructure.persistence.CategoryMapping import CategoryMapping
from modules.students.infrastructure.persistence.StudentMapping import StudentMapping
from modules.schools.infrastructure.persistence.SchoolMapping import SchoolMapping
import uuid
from datetime import datetime
from modules.events.controllers.routes import eventos_bp
from modules.user.controllers.routes import users_bp




def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(eventos_bp, url_prefix="/eventos")
    app.register_blueprint(areas_bp ,url_prefix="/area")
    app.register_blueprint(users_bp)

    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
