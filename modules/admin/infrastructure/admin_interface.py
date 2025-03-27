from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from shared.extensions import db
from modules.user.infrastructure.models import User

admin = Admin(name='Skyfall Admin', template_mode='bootstrap4')

def init_admin(app):
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
