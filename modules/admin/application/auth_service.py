from flask import session, redirect, url_for
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository

user_repo = PostgresUserRepository()

def authenticate_admin(email, password):
    user = user_repo.find_by_email(email)
    if not user:
        return None
    if not check_password_hash(user.password, password):
        return None
    return user

def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("admin_user")
        if not user_id:
            return redirect(url_for("admin_bp.login"))
        user = user_repo.find_by_id(user_id)
        if user:
            return f(*args, **kwargs)
        return redirect(url_for("admin_bp.login"))
    return decorated_function
