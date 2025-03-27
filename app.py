from flask import Flask
from config import Config
from shared.extensions import db, migrate, jwt
from modules.user.controllers.routes import user_bp
from modules.home.controllers.routes import home_bp
from modules.admin.infrastructure.admin_interface import init_admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    init_admin(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
