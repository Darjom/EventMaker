from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

def login_user(email, password, repo):
    user = repo.get_by_email(email)
    if not user or not check_password_hash(user.password, password):
        return None
    token = create_access_token(identity={"id": user.id, "role": user.role})
    return token
