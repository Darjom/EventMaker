from flask import session, redirect, url_for
from functools import wraps
from werkzeug.security import check_password_hash
from modules.user.infrastructure.persistence.UserMapping import UserMapping

def authenticate_admin(email, password):
    user = UserMapping.query.filter_by(email=email).first()
    if not user:
        return None
    if not any(role.name == 'administrativo' for role in user.roles):
        return None
    if not check_password_hash(user.password, password):
        return None
    return user

def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('admin_bp.login'))

        user = UserMapping.query.get(user_id)
        if user and any(role.name == 'administrativo' for role in user.roles):
            return f(*args, **kwargs)
        return redirect(url_for('admin_bp.login'))
    return decorated_function
