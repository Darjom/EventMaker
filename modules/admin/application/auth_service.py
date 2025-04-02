from werkzeug.security import check_password_hash
from modules.user.infrastructure.models import User

def authenticate_admin(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    if user.role != "administrativo":
        return None
    if not check_password_hash(user.password, password):
        return None
    return user
